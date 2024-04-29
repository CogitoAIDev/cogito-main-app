from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.chains import LLMChain
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.outputs import LLMResult
from langchain_core.prompts import MessagesPlaceholder
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor


from Prompts import GoalsClassificationPrompt, GoalsClassificationObject, GoalsCLassificationParser
from Prompts import FirstStepClassificationPrompt, FirstStepClassificationObject, FirstStepParser
from Prompts import JustChatPrompt
from Prompts import AddingGoalAgentPrompt
from Messager import send_message, Message
from Tools import AddGoalTool

import asyncio
import aiofiles
from typing import Any, Dict, List

from dotenv import load_dotenv
import os

from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages

load_dotenv()

# Seeting up LangChain logs. https://smith.langchain.com
LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=os.getenv("LANGSMITH_API_KEY")
LANGCHAIN_PROJECT="cogitodev"





# Initializing LLM model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm3 = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.2, model='gpt-3.5-turbo-0125')



 
class IncomingMessage:
    """
    Incoming message from the user and its processing inside.
    Attributes:
        user_id (int): User's tg chat id, same as the user_id in the DB.
        text (str): Text that user sent to us.
        chat_history (to be decided): chat_history

    """

    def __init__(self, user_id, text, chat_history):
        self.user_id = user_id
        self.text = text
        self.history = chat_history
        
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.user_id
        del self.text
        del self.history

        
    async def goals_processor(self):

        # Goals CLassification chain
        ChainGoalsClassification = GoalsClassificationPrompt | llm3 | GoalsCLassificationParser

        output = await ChainGoalsClassification.ainvoke({"input": self.text, "chat_history": self.history, "format_instructions":GoalsCLassificationParser.get_format_instructions() })
        if output.type == 'add' or output.type == 'Add':
            await self.goals_add_processor()
        else:
            message = Message(chat_id=self.user_id, text=output.type + " " + format(output.certainty , ".2f"))
            await send_message(message)



    async def goals_add_processor(self):
        tool = AddGoalTool()
        agent = create_tool_calling_agent(llm3, tools= [tool ], prompt=AddingGoalAgentPrompt)
        agent_executor = AgentExecutor(agent=agent, tools= [tool], verbose=True)
        output = agent_executor.ainvoke({"input": self.text,"user_id": self.user_id, "chat_history": self.history})
        message = Message(chat_id=self.user_id, text=output)
        await send_message(message)
        




    async def chat_processor(self):
         
        # Just Chat chain
        ChainJustChat = JustChatPrompt | llm3

        output = await ChainJustChat.ainvoke({"input": self.text, "chat_history": self.history})
        message = Message(chat_id=self.user_id, text=output.content)
        await send_message(message)

    

    async def start_processing(self):

        # First Step Classification chain
        Chain1 = FirstStepClassificationPrompt | llm3 | FirstStepParser
        
        output = await Chain1.ainvoke({"input": self.text, "chat_history": self.history, "format_instructions":FirstStepParser.get_format_instructions() })
        if output.type=='goals': 
            await self.goals_processor()
        else:
            await self.chat_processor()

        

        

# Starting the LLM process
async def start(user_id, text):

    # we need to get_chat_history here
    history=  [("human", "hello"), ("ai", "hello")]

    with IncomingMessage(user_id, text, chat_history=history) as messageInput:
        await messageInput.start_processing()

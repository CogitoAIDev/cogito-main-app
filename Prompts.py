from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

#### GOAL CLASSIFICATION 

# Prompt for Goal classification
GoalsClassificationPrompt = ChatPromptTemplate.from_messages( [
    (
            "system",
            "You are an AI mentor that helps people stay motivated, so you store their goals. In this message user showed a desire to do something with his goals. It can be one of the following options: Change already stored goals, Add a new goal, Delete some stored goal, or show some stored goals. If nothing out of stated actions are relevant, just return No Action. Consider chat's history when deciding. . \n{format_instructions} \n The users message is following: {input} "
        ), 
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
]
)

# Object with data that we got from the first step, which decides, what is the main topic of the message
class GoalsClassificationObject(BaseModel):
    type: str = Field(description="You need to store only one word. change if user wants to change goals (for example he wants to complete only half of the course, bot the full), add if user wants to add a new one, delete if user wants to delete, show if user wants you to show his goals and noaction if noaction is implied. ")
    certainty: float = Field(description="From 0 to 1, how certain are you that you selected the right category for the message?")

# Goals classification parser
GoalsCLassificationParser = PydanticOutputParser(pydantic_object=GoalsClassificationObject)




#### FIRST STEP CLASSFICATION 

# Prompt for first step
FirstStepClassificationPrompt = ChatPromptTemplate.from_messages( [
    (
            "system",
            "You are an AI mentor that helps people stay motivated, so you store their goals. You need to decide whether the message you got from the user is about their specific goals, may be they want to add a new goal, or to extract an exisiting one, or whether they just want to chat. Consider chat's history if provided. In the first case return just word goals. In other case return word chat. \n{format_instructions} \n The users message is following: {input} "
        ), 
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
]
)

# Object with data that we got from the first step, which decides, what is the main topic of the message
class FirstStepClassificationObject(BaseModel):
    type: str = Field(description="Either chat or goals")
    certainty: float = Field(description="From 0 to 1, how certain are you that you selected the right category for the message?")

# Parser for getting this object out of text
FirstStepParser = PydanticOutputParser(pydantic_object=FirstStepClassificationObject)




#### JUST CHAT

# Prompt for just chat
JustChatPrompt = ChatPromptTemplate.from_messages( [
    (
            "system",
            "You are an AI mentor that helps people stay motivated. Answer to the user according to this description. The users message is following: {input} "
        ), 
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
]
)


#### ADDING GOAL AGENT

# Prompt for adding goal agent
AddingGoalAgentPrompt = ChatPromptTemplate.from_messages( [
    (
            "system",
            "You are an AI mentor that helps people stay motivated. User wants to add a new goal, therefore check if a user"+
            "has provided all the required info. Required info: description of the goal, end of goal (under what circumstances should the goal be considered finished and achieved). If the user hasnt provided all the info, explicitly ask him for the needed data, that he hasnt provided. The id of the user if: {user_id}. Consider also chat history, required info can already be there: {chat_history}. The users message is following: {input} "
        ), 
        ("placeholder", "{chat_history}"),
        MessagesPlaceholder("agent_scratchpad"),
        ("human", "{input}"),
]
)
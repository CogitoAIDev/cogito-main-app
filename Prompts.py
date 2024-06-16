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
            "You are an AI mentor that helps people stay motivated, so you have acess to their stored goals (global goals which user wants to achieve), events (specific actions, pieces of work user needs to take). You need to take a look at users new message and at chat history."+
            "Based on the content of the message and the history, you need to classify what you should do. There are following options:" +
            "1) Just Chat. If person just wants to chat with you, user doesnt want to do something with their goals and their events and you dont need any additional information about the user to answer the users message. In this case return just one word: CHAT" +
            "2) Do something with users global goals. If you need to have an access to database with stored users goals to answer the message or to save information then choose this option. Examples: user wants to add a new goal; user wants to retrieve their goals; user wants to change their goals; user wants to delete their goal; user wants to discuss precisely their goal. Be careful, goals might seem similar to the next option events, but goals are more global, long-term. In this case return one word: GOALS" +
            "3) Do something with users events. If you need to have an access to database with stored user events to answer the message or to save information then choose this option. Events are small specific actions user do regularly or not regularly. For example: watch a lecture; attend a conference; finish homework. So user might want to take following actions: add a new event; change current events; change the frequency or timetable of existent events. In this case return one word: EVENTS " + 
            "{format_instructions} \n The users message is following: {input} "
        ), 
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
]
)

# Object with data that we got from the first step, which decides, what is the main topic of the message
class FirstStepClassificationObject(BaseModel):
    type: str = Field(description="CHAT, GOALS or EVENTS")
    certainty: str = Field(description="Fill in how certain are you in your decision: NOT_CERTAIN, HALF_CERTAIN, CERTAIN " )

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


#### ADDING EVENT AGENT

# Prompt for adding event agent
AddingGoalAgentPrompt = ChatPromptTemplate.from_messages( [
    (
            "system",
            "You are an AI mentor that helps people stay motivated. User wants to add a new event (specific actions, pieces of work user needs to take), therefore check if a user"+
            "has provided all the required info. Required info: description of the event, frequency of this event (one-time event, regular event, regular event for some time of period, etc.) and timetable of this event (when should this event be executed) . If the user hasnt provided all the info, explicitly ask him for the needed data, that he hasnt provided. The id of the user if: {user_id}. Consider also chat history, required info can already be there: {chat_history}. The users message is following: {input} "
        ), 
        ("placeholder", "{chat_history}"),
        MessagesPlaceholder("agent_scratchpad"),
        ("human", "{input}"),
]
)
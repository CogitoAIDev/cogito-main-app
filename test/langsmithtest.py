import openai
from langsmith.wrappers import wrap_openai
from langsmith import traceable
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Seeting up LangChain logs. https://smith.langchain.com



import os
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = "cogitodev"


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
import uuid
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
model = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0.2, model='gpt-3.5-turbo-0125')
prompt = ChatPromptTemplate.from_messages([('placeholder', "{messages}")])
chain = prompt | model
messages = [HumanMessage(content="hi! I'm bob")]
config = {"metadata": {"conversation_id": str(uuid.uuid4())}}
response = chain.invoke({"messages": messages}, config=config)
messages = messages + [response, HumanMessage(content="whats my name")]
response = chain.invoke({"messages": messages}, config=config)
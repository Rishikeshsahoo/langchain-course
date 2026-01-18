from langsmith import Client
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

llm= ChatOpenAI(model_name="gpt-5-nano")

client=Client()
prompt=client.pull_prompt("rlm/rag-prompt")

generation_chain= prompt | llm | StrOutputParser()

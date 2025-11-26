import requests
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from data import data
load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

template = """
Hi you are a summary agent and your task is to summarize the given data.
below I am providing you the data

{data}

now summarize this data.
"""
def main():
    prompt = PromptTemplate(input_variables=["data"], template=template)
    chain = prompt | llm
    res=chain.invoke(input ={"data":data})
    print(res.content)
    with open("summary.txt", "w") as f:
        f.write(res.content)


 
if __name__ == "__main__":
    main()

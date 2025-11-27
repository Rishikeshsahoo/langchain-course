from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from langchain.tools import tool
from lib import system_prompt, question_prompt
from langchain.messages import HumanMessage
import json
from pydantic import BaseModel, Field
from typing import List



# _______________________________This is the pydantic model_____________________________
class Source(BaseModel):
    """source of the information from the internet"""
    source:str= Field(description="source of the information from the internet")
class AgentResponse(BaseModel):
    """This class consosts of the response from the agent, the agent is supposed to fill the information in this 
    format only"""

    data:str=Field(description="This is the main response from the agent in the markdown format (make sure it is in markdown)")
    sources:List[Source]=Field(description="list of sources")



# ____________________________________This is the llm_________________________________
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=8096,  # Set explicit token limit for longer responses
    timeout=None,
    max_retries=2,
)


# __________________________________This is the tool_________________________________
tavily_search = TavilySearch(
    max_results=5,
    topic="general"
)

@tool
def search_tool(query:str)->str:
    """this is a tool to search the internet for the given query
    Args:
        query (str): query to search
    Returns:
        str: response from the search
    """
    print(f"searching the internet for ...{query}")
    response= tavily_search.invoke({"query": query})
    return response


# __________________________________This is the main function_________________________________
def main():
    print("Thinking...")
    tools=[search_tool]
    agent= create_agent(model=llm,tools=tools, system_prompt=system_prompt,  response_format=AgentResponse)
    response=agent.invoke({"messages":[HumanMessage(content=question_prompt)]})
    data=response.get('structured_response')
    main_data=data.data
    sources=data.sources
    
    # Write the agent response to output.md
    with open("output.md", "w", encoding="utf-8") as f:
        # Write the main data (markdown content)
        f.write(main_data)
        f.write("\n\n")
        
        # Write the sources section
        f.write("---\n\n")
        f.write("## Sources\n\n")
        for idx, source in enumerate(sources, 1):
            f.write(f"{idx}. {source.source}\n")
    
    print("✅ Data successfully written to output.md")
 

    
if __name__ == "__main__":
    main()

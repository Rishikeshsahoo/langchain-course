from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI

@tool
def triple(num:float) -> float:
    """
    This is a tool that can be used to triple a number i.e. multiple a number by 3
    (1) Multiplies the provided number by three.
    (2)Triples the number passed to it
    Args:
        num (float): The number to be tripled.

    Returns:
        float: The input number multiplied by three.
    """
    return num * 3

tools=[TavilySearch(max_results=2), triple]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

llm_with_tools=llm.bind_tools(tools)

from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI

@tool
def triple(num:float) -> float:
    """
    Multiplies the provided number by three.

    Args:
        num (float): The number to be tripled.

    Returns:
        float: The input number multiplied by three.
    """
    return num * 3

tools=[TavilySearch(max_results=1), triple]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

llm_with_tools=llm.bind_tools(tools)
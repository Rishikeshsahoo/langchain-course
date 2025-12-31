from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from react import llm_with_tools,tools

from dotenv import load_dotenv
load_dotenv()

SYSTEM_PROMPT = """You are a helpful assistant that can use tools to answer user questions.
you have tools for performing all the tasks given to you
use those tools to give the final output
"""

# This will be a node
def run_agent_reasoning(state:MessagesState):
    response=llm_with_tools.invoke([{"role":"system","content":SYSTEM_PROMPT},*state['messages']])
    return {"messages":response}

tool_node=ToolNode(tools)
    
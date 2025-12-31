from typing import Literal
from dotenv import load_dotenv
load_dotenv()   

from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, START,END

from nodes import run_agent_reasoning, tool_node
from logger import log_info
AGENT_REASON="run_agent_reasoning"
TOOLS="tool_node"
LAST=-1

def should_continue(state:MessagesState)->Literal[TOOLS, END]:
    if(state['messages'][-1].tool_calls):
        return TOOLS
    return END

flow= StateGraph(MessagesState)

flow.add_node(AGENT_REASON,run_agent_reasoning)
flow.add_node(TOOLS,tool_node)

flow.add_edge(START,AGENT_REASON)
flow.add_conditional_edges(AGENT_REASON,should_continue)
flow.add_edge(TOOLS, AGENT_REASON)

graph= flow.compile()

graph.get_graph().draw_mermaid_png(output_file_path="flow.png")


response=graph.invoke({"messages":[HumanMessage(content="What is the temprature in London (United Kingdom) today?, Tripple it and give me the answer!")]} )

log_info(response['messages'][-1].content)


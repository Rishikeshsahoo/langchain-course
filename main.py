from typing import Literal
from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import BaseMessage,HumanMessage
from langgraph.graph import END, StateGraph, MessagesState

# A reducer is a function 
# that tells how to update the state flowing in the graph
from langgraph.graph.message import add_messages

from chains import reflection_chain, generation_chain


def generate_node(state:MessagesState):
    generated_response = generation_chain.invoke({"messages":state["messages"]})
    return {"messages":[generated_response]}

def reflect_node(state:MessagesState):
    reflection_response = reflection_chain.invoke({"messages":state["messages"]})
    return {"messages":[HumanMessage(content=reflection_response.content)]}

builder= StateGraph(MessagesState)
builder.add_node("GENERATE", generate_node)
builder.add_node("REFLECT",reflect_node)

def should_continue(state:MessagesState)->Literal["REFLECT",END]:
    if(len(state["messages"])>7):
        return END
    return "REFLECT"

builder.set_entry_point("GENERATE")
builder.add_conditional_edges("GENERATE",should_continue)
builder.add_edge("REFLECT","GENERATE")
graph=builder.compile()

print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

if __name__ == "__main__":
    print("Hello langgraph")
    inputs = {
    "messages": [
        HumanMessage(
            content="""Make this tweet better:"
                                @LangChainAI
        — newly Tool Calling feature is seriously underrated.

        After a long wait, it's  here- making the implementation of agents across different models with function calling - super easy.

        Made a video covering their newest blog post

                                """
        )
    ]
    }
    final_response = graph.invoke(inputs)
    print(final_response)


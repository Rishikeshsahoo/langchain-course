from typing import List

from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()



# this is the tool decorator
# this decorate function and make it callable by llm
# https://docs.langchain.com/oss/python/langchain/tools

def find_tool_by_name(tools:List[Tool], tool_name:str)->Tool:
    for selected_tool in tools:
        if selected_tool.name == tool_name:
            return selected_tool
    raise ValueError(f"Tool {tool_name} not found")

@tool
def get_text_length(text:str)->int:
    """
    Return the length of text
    
    Args:
        text (str): The text to be processed
    
    Returns:
        int: The length of the text
    """
    return len(text)


def main():
    tools=[get_text_length]

    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    tool_calling_llm=llm.bind_tools(tools)

    messages=[
        SystemMessage(content="""You are a helpful AI assistant with access to tools. 
When asked a question, use the available tools if needed to gather information.
After using a tool, always provide a clear, natural language answer to the user's question.
Be concise and helpful in your responses."""),
        HumanMessage(content="What is the length of the text : Hello World")
    ]

    while True:
        response= tool_calling_llm.invoke(messages)
        print("a")
        print(response)
        if(response.type=="ai" and response.tool_calls and len(response.tool_calls)>0):
            messages.append(response)
            for tool_call in response.tool_calls:
                print("b")
                print((tool_call))
                tool_name=tool_call.get("name")
                tool_args=tool_call.get("args")
                tool_id=tool_call.get("id")
                selected_tool= find_tool_by_name(tools, tool_name)
                tool_result=selected_tool.invoke(tool_args)
                messages.append(ToolMessage(content=str(tool_result), tool_call_id=tool_id))
            continue
            
        messages.append(response)
        print(response.content)
        break
    print(messages)

if __name__ == "__main__":
    main()

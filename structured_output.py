from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from prompts import main_prompt
from schema import AgentResponse

from dotenv import load_dotenv
load_dotenv()

tavily_search = TavilySearch(max_results=5, topic="general")

tools=[tavily_search]
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)
structured_llm= llm.with_structured_output(AgentResponse)

react_prompt_with_format_instructions= PromptTemplate(
    template=main_prompt, 
    input_variables=["input", "agent_scratchpad", "tool_names"]
    ).partial(format_instructions= "")



agent= create_react_agent(llm=llm, tools=tools, prompt=react_prompt_with_format_instructions)
agent_executor= AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
fetch_output= RunnableLambda(lambda x: x["output"])


chain= agent_executor | fetch_output | structured_llm
def main():
    result= chain.invoke(input={"input": "What are the latest news about AI in the world"})
    print(result)

if __name__ == "__main__":
    main()

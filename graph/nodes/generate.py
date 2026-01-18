from dotenv import load_dotenv
load_dotenv()
from graph.state import GraphState
from graph.chains import generation_chain


def generate(state:GraphState) -> dict:
    question= state['question']
    documents= state['documents']
    
    response= generation_chain.invoke({"context":documents,"question":question})

    return {"generation":response}
    
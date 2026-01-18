from dotenv import load_dotenv
load_dotenv()
from langgraph.graph import StateGraph,END,START
from graph.state import GraphState
from graph.nodes import retrieve,grade_documents,generate,web_search
from graph.const import RETRIEVE,GRADE_DOCUMENTS,GENERATE,WEBSEARCH
from typing import Literal

def decide_to_generate(state:GraphState) -> Literal[WEBSEARCH,GENERATE]:
    if(state['web_search']):
        print("NOT ALL DOCUMENTS ARE RELEVANT SO WEB SEARCH")
        return WEBSEARCH

    print("ALL DOCUMENTS ARE RELEVANT SO GENERATE")
    return GENERATE

workflow=StateGraph(GraphState)

workflow.add_node(RETRIEVE,retrieve)
workflow.add_node(GRADE_DOCUMENTS,grade_documents)
workflow.add_node(GENERATE,generate)
workflow.add_node(WEBSEARCH,web_search)

workflow.add_edge(START,RETRIEVE)
workflow.add_edge(RETRIEVE,GRADE_DOCUMENTS)
workflow.add_conditional_edges(GRADE_DOCUMENTS,decide_to_generate)
workflow.add_edge(WEBSEARCH,GENERATE)
workflow.add_edge(GENERATE,END)

app=workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")

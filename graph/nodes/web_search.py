from langchain_tavily import TavilySearch
from typing import Dict, Any
from langchain_core.documents import Document
from graph.state import GraphState

search_tool=TavilySearch( max_results=3)

def web_search(state:GraphState) -> Dict[str, Any]:
    search_results=search_tool.invoke({"query":state['question']})["results"]
    
    single_doc_content= "\n".join([search_result['content'] for search_result in search_results])
    search_result_document=Document(page_content=single_doc_content)

    documents= state['documents']
    if documents is None:
        documents=[]
    documents.append(search_result_document)
    return {'documents':documents}
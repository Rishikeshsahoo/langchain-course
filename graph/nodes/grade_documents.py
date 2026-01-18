from typing import Dict, Any
from graph.state import GraphState
from graph.chains.retreival_grader import grader_chain

def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """
    filtered_docs=[]
    web_search=False
    documents=state['documents']
    question= state['question']
    for d in documents:
        grade= grader_chain.invoke({"document":d,"question":question})
        if grade.binary_score.lower() == 'yes':
            print("relevant document found")
            filtered_docs.append(d)
        else:
            print("irrelevant document found")
            web_search=True
    return {'documents':filtered_docs,'web_search':web_search}
            

        
    

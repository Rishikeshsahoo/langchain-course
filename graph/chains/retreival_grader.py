from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain.messages import HumanMessage, AIMessage, SystemMessage     
llm = ChatOpenAI(model_name="gpt-5-nano")

class DocumenGradeJudgement(BaseModel):
    binary_score:str = Field(description='''
    this is the binary score of the document
    it means whether the passed document is relevant to the question or not
    it can be either 'yes' or 'no' ''')

structured_llm_grader= llm.with_structured_output(DocumenGradeJudgement)

system_message="""You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

# Create a prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_message),
    ("human", "Retrieved document: \n\n {document} \n\n User question: {question}")
])
# Chain the prompt with the structured LLM
grader_chain = prompt | structured_llm_grader
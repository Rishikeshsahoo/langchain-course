import os
from operator import itemgetter
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore

load_dotenv()

prompt_template = ChatPromptTemplate.from_messages(
    [
        ("human", """Answer the question based on the context provided.
    Context: {context}

    Question: {question}

    Provide a detailed answer.""")
    ]
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
    max_retries=2,
)
embeddings= GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore = PineconeVectorStore(index_name=os.getenv("INDEX_NAME"), embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
def format_documents(documents):
    return "\n".join([doc.page_content for doc in documents])


def retrieval_chain_without_lcel(query: str):
    """
    Simple retrieval chain without LCEL.
    Manually retrieves documents, formats them, and generates a response.

    Limitations:
    - Manual step-by-step execution
    - No built-in streaming support
    - No async support without additional code
    - Harder to compose with other chains
    - More verbose and error-prone
    """
    # step 1: retrieve documents
    docs= retriever.invoke(query)
    # step 2: format documents
    formatted_docs= format_documents(docs)
    # step 3: format prompt
    prompt= prompt_template.format_messages(context=formatted_docs, question=query)
    # step 4: generate response
    response= llm.invoke(prompt)
    return response.content


def retrieval_chain_with_lcel():
    # now we only need to invoke the chain with a "question"
    # and the RunnablePassthrough.assign will add a context to the input
    # and return a runnable that can be passed next to the chain
    retrieval_chain= (
        RunnablePassthrough.assign(
            context= (lambda x: x["question"])| retriever | format_documents
        ) |
        prompt_template |
        llm |
        StrOutputParser()
    )
    
    return retrieval_chain
    

if __name__== "__main__":
    # =============without langchain expression language==============
    print("\n"+"="*70)
    print("Retrieval chain without LCEL")
    print("="*70+"\n")
    query= "what is RAG and what are the challengs in RAG ?"
    response= retrieval_chain_without_lcel(query)
    print("\nAnswer:")
    print(response)
    # =============without langchain expression language==============

    # =============with langchain expression language==============
    print("\n"+"="*70)
    print("Retrieval chain with LCEL")
    print("="*70+"\n")
    retrieval_chain= retrieval_chain_with_lcel()
    query= "what is RAG and what are the challengs in RAG ?"
    response= retrieval_chain.invoke({"question": query})
    print("\nAnswer:")
    print(response)

    # =======with langchain expression language=========
    


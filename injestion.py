import os
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

if __name__ =="__main__":
    loader= TextLoader("./meduim_blog.txt")
    document= loader.load()

    print("loading...")
    
    text_splitter= RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    texts= text_splitter.split_documents(document)
    print("injesting...")
    PineconeVectorStore.from_documents(texts, embeddings, index_name=os.getenv("INDEX_NAME"))
    print("done")
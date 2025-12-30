import asyncio
import os
import ssl
import certifi
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap

from logger import (Colors, log_error, log_header, log_info, log_success, log_warning)

load_dotenv()


ssl_context=ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

embedding= GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorestore= PineconeVectorStore(
    index_name=os.environ["INDEX_NAME"],
    embedding=embedding
)

tavily_extract= TavilyExtract()
tavily_map= TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl= TavilyCrawl()

async def main():
    log_header("Document injestion pipeline")

    log_info("Starting Tavily Crawl: for https://docs.langchain.com/oss/python/langchain/overview", Colors.PURPLE)
    res= tavily_crawl.invoke({
        "url":"https://docs.langchain.com/oss/python/langchain/overview",
        "max_depth":3,
        "extract_depth":"advanced"
    })
    all_docs= [Document(page_content=str(result["raw_content"]), metadata={"source":result["url"]}) for result in res["results"]]
    log_success(f"Successfully crawled {len(all_docs)} documents")
    
if __name__ == "__main__":
    asyncio.run(main())
    
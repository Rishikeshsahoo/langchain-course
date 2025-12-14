from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


load_dotenv()

def check_dimension(model_name):
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model=model_name)
        vector = embeddings.embed_query("test")
        print(vector)
        print(f"Model: {model_name}, Dimension: {len(vector)}")
    except Exception as e:
        print(f"Model: {model_name} failed: {e}")

if __name__ == "__main__":
    # check_dimension("models/embedding-001")
    check_dimension("models/gemini-embedding-001")

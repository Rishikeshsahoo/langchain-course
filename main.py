from dotenv import load_dotenv
load_dotenv()
from graph.workflow import app


if __name__ == "__main__":
    print(app.invoke({"question":"What is agent memory ?"}))
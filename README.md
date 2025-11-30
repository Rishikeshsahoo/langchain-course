# LangChain ReAct Agent Course

Welcome to the LangChain ReAct Agent Course repository! This project demonstrates how to build powerful AI agents using LangChain, Tavily Search, and Google Gemini.

## 🚀 Key Features

- **ReAct Agent Architecture**: Implements the Reasoning and Acting (ReAct) pattern for intelligent problem-solving.
- **Real-time Search**: Integrates **Tavily Search** to fetch the latest information from the web.
- **Google Gemini**: Powered by the **gemini-2.5-flash** model for fast and accurate responses.
- **Structured Output**: Demonstrates two robust methods for getting structured JSON responses from LLMs:
    - Traditional `PydanticOutputParser`
    - Modern `.with_structured_output()` method

## 📂 Project Structure

Here's a quick overview of the key files in this repository:

- **`main.py`**: The entry point for the traditional ReAct agent implementation.
- **`structured_output.py`**: A streamlined implementation using the newer `with_structured_output` capability.
- **`schema.py`**: Defines the Pydantic models (`AgentResponse`, `Source`) to ensure type-safe data structures.
- **`prompts.py`**: Contains the custom prompt templates used to guide the agent.

## 📓 Interactive Notebooks

We have nicely managed notebooks to help you understand the implementation better. These are highly recommended for learning the core concepts step-by-step:

### 1. [Traditional Agent Walkthrough](traditional_agent.ipynb)
A comprehensive guide covering:
- Setting up the environment and tools.
- Understanding `PydanticOutputParser` and `PromptTemplate.partial()`.
- Building the agent loop with `AgentExecutor`.
- **Debugging**: How to handle parsing errors and visualize the agent's thought process.

### 2. [Structured Output Guide](with_structured_output.ipynb)
A modern approach tutorial that shows:
- How to use `llm.with_structured_output()` for cleaner code.
- Comparing manual parsing vs. native structured output.
- Building a reliable chain without complex prompt engineering.

## 🛠️ Getting Started

1. **Install Dependencies**:
   ```bash
   poetry install
   ```

2. **Set up Environment**:
   Create a `.env` file and add your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

3. **Run the Agent**:
   ```bash
   python main.py
   ```

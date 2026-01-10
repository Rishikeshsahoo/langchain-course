from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

reflection_prompt= ChatPromptTemplate.from_messages([
    ("system",
    "You are a viral twitter influencer grading a tweet. Generate critique for the tweet and recommendations for the user."
    "always provide detailed critique and recommendations."
    "you may include recommendations for hashtags, content, and style for virality and reach"
   
    ),
    MessagesPlaceholder(variable_name="messages")
])

generation_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a viral twitter influencer assistant. Generate a new improved tweet based on the critique and recommendations provided. "
     "The tweet should be engaging, concise, and optimized for virality. "
     "Include relevant hashtags and emojis where appropriate. "
     "Keep the tweet under 280 characters."
     "Do not give choices of multiple options, only give one tweet at a time (VERY IMPORTANT)"
    ),
    MessagesPlaceholder(variable_name="messages")
])

llm =ChatGoogleGenerativeAI(model="gemini-2.5-flash")
reflection_chain= reflection_prompt | llm
generation_chain = generation_prompt | llm
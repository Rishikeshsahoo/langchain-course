from pydantic import BaseModel, Field
from typing import List


class Source(BaseModel):
    url: str = Field(description="URL of the source")


class AgentResponse(BaseModel):
    answer: str = Field(description="agent's answer to the question")
    sources: List[Source] = Field(default_factory=list, description="List of sources used to answer the question")
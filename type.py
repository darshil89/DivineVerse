from pydantic import BaseModel, Field


class God(BaseModel):
    belongs_to: str = Field(..., description="The name of the god")
    name: str = Field(..., description="The name of the god")
    meaning: str = Field(..., description="The meaning of the god")
    mantra: str = Field(..., description="The mantra of the god")
    sanskrit: str = Field(..., description="The sanskrit of the god")

class ChatRequest(BaseModel):
    text: str = Field(..., description="The text to chat about")
    
    
class GetEmbeddingsRequest(BaseModel):
    name: str = Field(..., description="The name of the god")
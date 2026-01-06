from pydantic import BaseModel

class AIRequest(BaseModel):
    event: str
    details: str

class AIResponse(BaseModel):
    result: str

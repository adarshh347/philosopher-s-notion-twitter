from pydantic import BaseModel
class ChatRequest(BaseModel):
    user_message:str
    persona_id:str

class ChatResponse(BaseModel):
    persona_reply: str

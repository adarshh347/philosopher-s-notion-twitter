from fastapi import APIRouter, Depends
from backend.app.models.chat_models import ChatRequest, ChatResponse
from backend.app.core.chat_service import ChatService, chat_service

router= APIRouter()

def get_chat_service():
    return chat_service

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
        request:ChatRequest,
        service: ChatService = Depends(get_chat_service)
):
    reply= await

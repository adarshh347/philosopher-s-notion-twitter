from fastapi import APIRouter
from backend.app.models.chat_models import ChatRequest, ChatResponse
from backend.app.core.graph_service import app_brain

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def handle_chat(request: ChatRequest):
    """
    Entry point for the 'Fluid Persona' chat.
    It uses the LangGraph 'app_brain' to route, assemble, and generate.
    """

    # 1. Prepare the input state
    inputs = {
        "user_query": request.user_message,
        # In a real app, you would fetch previous messages from DB here
        # and populate "messages": [HumanMessage(...), AIMessage(...)]
        "messages": []
    }

    # 2. Run the Graph (Groq will handle the thinking)
    # We use ainvoke for async performance
    result = await app_brain.ainvoke(inputs)

    # 3. Extract the final response
    return ChatResponse(persona_reply=result["final_response"])
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.v1.endpoints import chat

app=FastAPI(title="genai platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(chat.router,prefix="/api/v1", tags=["Chat"])

@app.get("/")
def read_root():
    return {"message": "GenAI Persona API is running."}

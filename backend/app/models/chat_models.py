from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from datetime import datetime
from pydantic import BaseModel  # <--- NEEDED for API Schemas


# ==========================================
#  1. DATABASE MODELS (SQLModel tables)
# ==========================================

# Link Table
class PersonaConceptLink(SQLModel, table=True):
    persona_id: UUID = Field(foreign_key="persona.id", primary_key=True)
    concept_id: UUID = Field(foreign_key="concept.id", primary_key=True)
    strength: float = Field(default=1.0)


# Core Entities
class Persona(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    base_system_prompt: str

    # The "Fluid" part (Stored as JSON)
    lenses: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))

    # The "Evolution"
    evolution_log: List[str] = Field(default=[], sa_column=Column(JSON))

    concepts: List["Concept"] = Relationship(back_populates="personas", link_model=PersonaConceptLink)


class Concept(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    definition: str
    vector_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)  # Fixed typo (was created_id)

    personas: List[Persona] = Relationship(back_populates="concepts", link_model=PersonaConceptLink)


# Chat Data
class Conversation(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)  # Fixed typo (was primary_keys)
    persona_id: UUID = Field(foreign_key="persona.id")
    user_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversation.id")
    sender: str
    text: str
    metadata_: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))


# ==========================================
#  2. API SCHEMAS (Pydantic DTOs)
#  These are used by chat.py for validation
# ==========================================

class ChatRequest(BaseModel):
    """What the Frontend sends to the Backend"""
    user_message: str
    persona_id: str = "default"  # We'll use this later to fetch the specific Persona


class ChatResponse(BaseModel):
    """What the Backend sends back to Frontend"""
    persona_reply: str
    active_lenses: Optional[List[str]] = []  # Helpful for debugging your logic
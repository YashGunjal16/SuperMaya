import datetime
from pydantic import BaseModel

# --- User Schemas ---
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    # Show the system prompt when returning a user
    system_prompt: str

    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    email: str | None = None

# --- Chat Interaction Schemas ---
class ChatInteractionBase(BaseModel):
    user_query: str

class ChatInteractionCreate(ChatInteractionBase):
    pass

class ChatInteraction(ChatInteractionBase):
    id: int
    ai_response: str | None = None
    created_at: datetime.datetime
    # Show the owner and feedback score in responses
    owner_id: int
    feedback_score: int

    class Config:
        from_attributes = True
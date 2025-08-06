import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Field for user-specific prompts
    system_prompt = Column(String, default="You are a helpful assistant.")
    
    # Defines the one-to-many relationship
    interactions = relationship("ChatInteraction", back_populates="owner")

class ChatInteraction(Base):
    __tablename__ = "chat_interactions"
    id = Column(Integer, primary_key=True, index=True)
    user_query = Column(String, index=True)
    ai_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Field for tracking user feedback
    feedback_score = Column(Integer, default=0) # -1 bad, 0 none, 1 good

    # Defines the many-to-one relationship
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="interactions")
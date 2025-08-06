from fastapi import FastAPI, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import PIL.Image
import io

# Local Imports
from app.core import security
from app.db import database, models, crud
from app.schemas import main_schemas
from app.agents.meta_agent import meta_agent_instance
from app.auth.dependencies import get_current_active_user

app = FastAPI(
    title="SuperMaya AI Platform - Standout Edition",
    description="A secure, multi-modal, agentic AI backend with user accounts and feedback.",
    version="1.2.0" # Version bump for real financial data
)

# --- CORS Middleware ---
origins = ["http://localhost:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Database Initialization ---
@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# --- Authentication Endpoints ---
@app.post("/auth/register", response_model=main_schemas.User, tags=["Authentication"])
async def register_user(
    user: main_schemas.UserCreate, 
    db: AsyncSession = Depends(database.get_db)
):
    """Create a new user account."""
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@app.post("/auth/token", response_model=main_schemas.Token, tags=["Authentication"])
async def login_for_access_token(
    db: AsyncSession = Depends(database.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Log in a user to get a JWT access token."""
    user = await crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# --- User Endpoints ---
@app.get("/users/me", response_model=main_schemas.User, tags=["Users"])
async def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    """Get the profile for the currently authenticated user."""
    return current_user

@app.put("/users/me/prompt", response_model=main_schemas.User, tags=["Users"])
async def update_system_prompt(
    prompt: str = Form(...),
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update the custom system prompt for the current user."""
    return await crud.update_user_prompt(db, user_id=current_user.id, prompt=prompt)

# --- Chat Endpoints (Corrected with `await`) ---
@app.post("/chat/text", response_model=main_schemas.ChatInteraction, tags=["Chat"])
async def chat_with_text(
    chat_input: main_schemas.ChatInteractionCreate,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Handles text-only conversations. The MetaAgent will classify intent."""
    # This now correctly awaits the async 'run' method
    agent_response = await meta_agent_instance.run(user_query=chat_input.user_query, system_prompt=current_user.system_prompt)
    
    response_json_string = agent_response.model_dump_json(indent=2)
    return await crud.create_chat_interaction(db, user_id=current_user.id, query=chat_input.user_query, response=response_json_string)

@app.post("/chat/image", response_model=main_schemas.ChatInteraction, tags=["Chat"])
async def chat_with_image(
    user_query: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Handles image-based conversations for the authenticated user."""
    image_data = await image.read()
    pil_image = PIL.Image.open(io.BytesIO(image_data))
    
    # This now correctly awaits the async 'run_vision_agent' method
    agent_response = await meta_agent_instance.run_vision_agent(user_query=user_query, image=pil_image, system_prompt=current_user.system_prompt)
    
    response_json_string = agent_response.model_dump_json(indent=2)
    return await crud.create_chat_interaction(db, user_id=current_user.id, query=user_query, response=response_json_string)

# --- Feedback & History Endpoints ---
@app.post("/chat/feedback", tags=["Chat"])
async def submit_feedback(
    interaction_id: int,
    is_good: bool,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Submit feedback on a specific chat interaction."""
    score = 1 if is_good else -1
    await crud.update_feedback_score(db, interaction_id=interaction_id, owner_id=current_user.id, score=score)
    return {"status": "Feedback received"}

@app.get("/chat/history", response_model=List[main_schemas.ChatInteraction], tags=["Chat"])
async def get_my_chat_history(
    skip: int = 0, 
    limit: int = 10,
    db: AsyncSession = Depends(database.get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get the chat history for the authenticated user."""
    return await crud.get_user_interactions(db, user_id=current_user.id, skip=skip, limit=limit)
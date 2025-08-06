from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from . import models
from app.schemas import main_schemas
from app.core.security import get_password_hash, verify_password

# --- User CRUD ---
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()
    
async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def create_user(db: AsyncSession, user: main_schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user_prompt(db: AsyncSession, user_id: int, prompt: str):
    db_user = await get_user(db, user_id)
    if db_user:
        db_user.system_prompt = prompt
        await db.commit()
        await db.refresh(db_user)
    return db_user

# --- Chat Interaction CRUD ---
async def create_chat_interaction(db: AsyncSession, user_id: int, query: str, response: str):
    db_interaction = models.ChatInteraction(
        user_query=query,
        ai_response=response,
        owner_id=user_id
    )
    db.add(db_interaction)
    await db.commit()
    await db.refresh(db_interaction)
    return db_interaction

async def update_feedback_score(db: AsyncSession, interaction_id: int, owner_id: int, score: int):
    result = await db.execute(
        select(models.ChatInteraction).filter(
            models.ChatInteraction.id == interaction_id,
            models.ChatInteraction.owner_id == owner_id
        )
    )
    db_interaction = result.scalars().first()
    
    if db_interaction:
        db_interaction.feedback_score = score
        await db.commit()
    return

async def get_user_interactions(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.ChatInteraction).filter(
            models.ChatInteraction.owner_id == user_id
        ).order_by(models.ChatInteraction.id.desc()).offset(skip).limit(limit)
    )
    return result.scalars().all()
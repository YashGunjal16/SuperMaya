from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the async engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Create a session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_db():
    """Dependency to get a DB session for each request."""
    async with AsyncSessionLocal() as session:
        yield session
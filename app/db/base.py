from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.orm import declarative_base

# Create the asynchronous engine for connecting to the database
engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

# Create a factory for asynchronous database sessions
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class that all ORM models will inherit from
Base = declarative_base()


async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
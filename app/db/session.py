from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from typing import AsyncGenerator

from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)


async_session_factory = async_sessionmaker[AsyncSession](bind=engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = async_session_factory()
    try:
        yield db
    finally:
        await db.close()

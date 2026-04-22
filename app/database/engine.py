from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from app.config import DB_URL
from app.database.models import Base

engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    """Jadvallarni yaratish."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Jadvallarni o'chirish (faqat test uchun)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

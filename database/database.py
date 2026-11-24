from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config.config import settings
from database.models import Base

async_engine = create_async_engine(url=settings.database_url_aiosqlite, echo=True)
session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
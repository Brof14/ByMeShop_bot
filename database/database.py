from config import config
from database.models import Base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(config.DB_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

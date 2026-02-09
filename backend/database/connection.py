from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from database.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://frauduser:fraudpass123@localhost:5432/fraud_detection")
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
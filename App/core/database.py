from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .config import settings

# 1. Database Configuration

engine = create_async_engine(settings.database_url.strip() , echo=False)
SessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
Base = DeclarativeBase()

class Base(DeclarativeBase):
    pass

# 4. Async Dependency
async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
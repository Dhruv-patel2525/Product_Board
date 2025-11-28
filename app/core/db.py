# app/core/db.py
from sqlmodel import SQLModel, Session
from app.core.config import get_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession


settings = get_settings()

# create SQLModel engine
engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# session generator
async def get_session() -> AsyncSession:

    async with async_session() as session:
        async with session.begin():     # <-- THIS creates and commits/rolls back the tx
            yield session

        # yield session



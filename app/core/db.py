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
    """
    Context-managed session for DB operations
    Usage:
        with get_session() as session:
            ...
    """
    async with async_session() as session:
        yield session


# optional: init DB (creates tables if not using Alembic)
async def init_db() -> None:
    """
    Create all tables in the database.
    Make sure all SQLModel models are imported before calling this function.
    """
    from app.models.todo import ToDo  # ensures all models are registered

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

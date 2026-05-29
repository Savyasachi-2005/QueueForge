from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


# Engine and session factory are created lazily so they can be initialized per-process.
engine = None  # type: Optional[object]
AsyncSessionLocal: Optional[async_sessionmaker] = None


def init_db_engine() -> None:
    """Create the async engine and session factory for the current process."""
    global engine, AsyncSessionLocal
    if engine is None:
        engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
        AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session for request-scoped use.

    Ensures the engine/sessionmaker have been initialized for the current process.
    """
    if AsyncSessionLocal is None:
        init_db_engine()

    async with AsyncSessionLocal() as session:  # type: ignore[misc]
        yield session

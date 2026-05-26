from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings


# Create an async SQLAlchemy engine using the Supabase PostgreSQL URL
engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)

# Async session factory for FastAPI dependency injection
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    """Yield an async database session for request-scoped use."""

    async with AsyncSessionLocal() as session:
        yield session

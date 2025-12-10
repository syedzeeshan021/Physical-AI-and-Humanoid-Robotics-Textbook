from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy import text

from src.core.config import settings
from src.core.base import Base

# Create async engine for PostgreSQL/Neon
# Handle SSL configuration for asyncpg - remove incompatible parameters
import urllib.parse

# Get the database URL and remove incompatible parameters
raw_url = settings.NEON_DATABASE_URL or settings.DATABASE_URL
if raw_url and ("sslmode=" in raw_url or "channel_binding=" in raw_url):
    # Parse the URL and remove problematic parameters
    parsed = urllib.parse.urlparse(raw_url)
    query_params = urllib.parse.parse_qs(parsed.query)

    # Remove problematic parameters
    if 'sslmode' in query_params:
        del query_params['sslmode']
    if 'channel_binding' in query_params:
        del query_params['channel_binding']

    # Reconstruct the query string without problematic parameters
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    database_url = urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment)
    )
else:
    database_url = raw_url

async_engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

# Import all models to ensure they're registered with Base
# This ensures that create_all() creates all tables
from src.models import chapter, embedding, chat_session, chat_message, user

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def init_db():
    """Initialize the database by creating all tables"""
    async with async_engine.begin() as conn:
        # Create all tables defined in models
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db_session():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
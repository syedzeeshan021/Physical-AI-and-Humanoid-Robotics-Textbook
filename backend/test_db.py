#!/usr/bin/env python3
"""
Test script to test database connection
"""

from sqlalchemy.ext.asyncio import create_async_engine
from src.core.config import settings

print("Testing database connection...")
print(f"Database URL: {settings.NEON_DATABASE_URL or settings.DATABASE_URL}")

try:
    # Try to create the engine
    engine = create_async_engine(
        settings.NEON_DATABASE_URL or settings.DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )
    print("Engine created successfully!")

    # Try to connect
    import asyncio

    async def test_connection():
        async with engine.begin() as conn:
            print("Connection successful!")
            # Run a simple query
            result = await conn.execute("SELECT 1")
            print(f"Query result: {result.fetchone()}")

    asyncio.run(test_connection())
    print("Database connection test completed successfully!")

except Exception as e:
    print(f"Error connecting to database: {e}")
    import traceback
    traceback.print_exc()
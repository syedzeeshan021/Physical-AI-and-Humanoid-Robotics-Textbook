#!/usr/bin/env python3
"""
Test script to test database connection using the updated database module
"""

from src.core.database import async_engine

print("Testing database connection with updated database module...")

try:
    # Try to connect using the updated engine from database.py
    import asyncio

    async def test_connection():
        print("Attempting to connect to database...")
        async with async_engine.begin() as conn:
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
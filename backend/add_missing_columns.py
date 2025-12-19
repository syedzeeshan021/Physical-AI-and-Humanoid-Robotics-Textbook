import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from src.core.database import async_engine

async def add_missing_columns():
    async with async_engine.begin() as conn:
        # Add auth_status column to users table if it doesn't exist
        try:
            await conn.execute(text("""
                ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_status VARCHAR DEFAULT 'unverified' NOT NULL
            """))
            print("Added auth_status column to users table")
        except Exception as e:
            print(f"Error adding auth_status column: {e}")

        # Add translation_usage_history column to users table if it doesn't exist
        try:
            await conn.execute(text("""
                ALTER TABLE users ADD COLUMN IF NOT EXISTS translation_usage_history JSON
            """))
            print("Added translation_usage_history column to users table")
        except Exception as e:
            print(f"Error adding translation_usage_history column: {e}")

        print("Column addition process completed")

if __name__ == "__main__":
    asyncio.run(add_missing_columns())
import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import init_db
from src.core.config import settings

async def run_init():
    print('Database URL:', settings.DATABASE_URL)
    print('Initializing database...')
    await init_db()
    print('Database initialized successfully')

if __name__ == "__main__":
    asyncio.run(run_init())
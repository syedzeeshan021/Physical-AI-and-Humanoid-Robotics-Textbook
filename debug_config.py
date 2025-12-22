import sys
import os
from pathlib import Path

# Get the project root (where this script is located)
project_root = Path(__file__).parent
print(f"Project root: {project_root}")

# Add the project root to Python path
sys.path.insert(0, str(project_root))

# Add the backend directory to Python path
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))

# Don't change the working directory to ensure .env from project root is loaded
print(f"Current working directory: {os.getcwd()}")

from src.core.config import settings

print("Debugging configuration:")
print(f"Current working directory: {os.getcwd()}")
print(f"AI_PROVIDER: {settings.AI_PROVIDER}")
print(f"GEMINI_API_KEY: {settings.GEMINI_API_KEY}")
print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY}")

# Let's also check the .env file in the current directory
env_path = Path(".env")
print(f"Looking for .env at current directory: {env_path.absolute()}")
print(f".env file exists: {env_path.exists()}")

if env_path.exists():
    print("Contents of .env file:")
    with open(env_path, 'r') as f:
        print(f.read())
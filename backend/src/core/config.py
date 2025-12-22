from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Textbook Generation API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database settings
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
    NEON_DATABASE_URL: Optional[str] = None

    # Qdrant settings
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: Optional[str] = None

    # OpenAI settings
    OPENAI_API_KEY: Optional[str] = None

    # Google Gemini settings
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Default to gemini-1.5-flash

    # AI Provider configuration (openai or gemini)
    AI_PROVIDER: str = "openai"  # Default to openai, can be "gemini"

    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]  # In production, specify actual origins

    # Rate limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour in seconds

    # Google Cloud Translation settings
    GOOGLE_CLOUD_PROJECT_ID: Optional[str] = None
    GOOGLE_CLOUD_TRANSLATE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
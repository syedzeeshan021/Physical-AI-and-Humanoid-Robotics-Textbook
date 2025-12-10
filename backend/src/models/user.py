from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from src.core.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=True)
    hashed_password = Column(String, nullable=True)  # Hashed password for authentication
    preferences = Column(JSON, nullable=True)  # User preferences (language, theme, etc.)
    progress = Column(JSON, nullable=True)    # Learning progress tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
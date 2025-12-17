from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timedelta
import uuid

from src.core.base import Base


class TranslationSession(Base):
    __tablename__ = "translation_sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)  # Foreign key to users table
    original_content_ref = Column(Text, nullable=False)  # Reference to the original English content
    translated_content = Column(Text, nullable=False)  # The translated Urdu content
    chapter_reference = Column(String, nullable=False)  # Identifier for the chapter being translated
    translation_timestamp = Column(DateTime, default=datetime.utcnow)  # When the translation was performed
    is_cached = Column(Boolean, default=True, nullable=False)  # Whether this translation is cached
    cache_expires_at = Column(DateTime, nullable=False)  # When the cached translation expires

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set cache expiration to 24 hours from creation if not already set
        if not self.cache_expires_at:
            self.cache_expires_at = datetime.utcnow() + timedelta(hours=24)
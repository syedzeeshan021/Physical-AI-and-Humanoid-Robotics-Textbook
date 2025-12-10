from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from src.core.base import Base


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Chapter content in markdown
    order = Column(Integer, nullable=False)  # Chapter sequence order
    word_count = Column(Integer, nullable=False)  # Number of words in chapter
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
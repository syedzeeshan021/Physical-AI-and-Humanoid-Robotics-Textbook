from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id"), nullable=False)  # Reference to chapter
    content = Column(Text, nullable=False)  # Text snippet for embedding
    # embedding_vector would be stored in Qdrant, not in PostgreSQL
    token_count = Column(Integer, nullable=False)  # Number of tokens in content
    created_at = Column(DateTime, default=datetime.utcnow)
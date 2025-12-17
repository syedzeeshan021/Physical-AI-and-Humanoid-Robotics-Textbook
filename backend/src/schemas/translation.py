from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID


class TranslateRequest(BaseModel):
    content: str
    chapter_id: str
    target_language: Optional[str] = "ur"


class TranslateResponse(BaseModel):
    translated_content: str
    session_id: UUID
    is_cached: bool = False
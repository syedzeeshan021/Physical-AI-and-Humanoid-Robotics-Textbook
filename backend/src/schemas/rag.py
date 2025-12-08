from pydantic import BaseModel
from typing import List, Optional


class RagQueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = None


class RagQueryResponse(BaseModel):
    response: str
    sources: List[str]
    session_id: Optional[str] = None
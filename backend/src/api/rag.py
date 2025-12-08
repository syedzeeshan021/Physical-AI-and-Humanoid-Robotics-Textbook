from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from src.schemas.rag import RagQueryRequest, RagQueryResponse
from src.services.rag_service import rag_service
from src.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/query", response_model=RagQueryResponse)
async def query_rag_endpoint(request: RagQueryRequest):
    """
    Query the RAG system with user input
    """
    try:
        # Call the RAG service to process the query
        result = await rag_service.process_query(
            query=request.query,
            session_id=request.session_id
        )

        return RagQueryResponse(
            response=result.get("response", ""),
            sources=result.get("sources", []),
            session_id=result.get("session_id", request.session_id)
        )
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail="Error processing query")
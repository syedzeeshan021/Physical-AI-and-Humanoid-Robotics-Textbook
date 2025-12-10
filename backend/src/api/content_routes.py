from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import get_current_user
from src.models.user import User
from src.services.content_service import content_service
from src.core.database import get_db_session
from pydantic import BaseModel

router = APIRouter(prefix="/content", tags=["content"])

class TranslateRequest(BaseModel):
    content: str
    target_language: str = "ur"

class PersonalizeRequest(BaseModel):
    content: str
    user_preferences: Dict[str, Any]

@router.post("/translate")
async def translate_content(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user)
):
    """Translate content to the target language"""
    translated_content = await content_service.translate_content(
        request.content,
        request.target_language
    )
    return {"translated_content": translated_content}

@router.post("/personalize")
async def personalize_content(
    request: PersonalizeRequest,
    current_user: User = Depends(get_current_user)
):
    """Personalize content based on user preferences"""
    personalized_content = await content_service.personalize_content(
        request.content,
        request.user_preferences
    )
    return {"personalized_content": personalized_content}

@router.post("/transform")
async def transform_content(
    request: TranslateRequest,
    personalize: bool = False,
    current_user: User = Depends(get_current_user)
):
    """Transform content with both translation and personalization if requested"""
    content = request.content

    # First personalize if requested
    if personalize and current_user.preferences:
        from src.services.content_service import content_service
        content = await content_service.personalize_content(content, current_user.preferences)

    # Then translate
    if request.target_language:
        content = await content_service.translate_content(content, request.target_language)

    return {"transformed_content": content}
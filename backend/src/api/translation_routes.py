from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.auth.auth_service import get_current_user
from src.models.user import User
from src.schemas.translation import TranslateRequest, TranslateResponse
from src.services.translation_service import TranslationService
from src.core.config import settings

# Create a limiter for translation endpoints
translation_limiter = Limiter(key_func=get_remote_address)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/translation",
    tags=["translation"]
)


@router.post("/translate", response_model=TranslateResponse)
@translation_limiter.limit("100 per hour")  # Limit to 100 requests per hour per IP
async def translate_content(
    request: TranslateRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Translate content to Urdu.
    """
    try:
        # Verify user has proper authentication status for translation
        if current_user.auth_status == 'unverified':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account must be verified to access translation feature"
            )

        translation_service = TranslationService()
        result = await translation_service.translate_content(
            user_id=current_user.id,
            content=request.content,
            chapter_id=request.chapter_id,
            target_language=request.target_language or "ur"
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Translation service unavailable"
        )



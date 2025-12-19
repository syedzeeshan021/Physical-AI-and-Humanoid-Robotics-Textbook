from typing import Optional
from datetime import datetime, timedelta
import logging
import uuid
import asyncio

from src.core.config import settings
from src.models.translation_session import TranslationSession
from src.models.user import User
from src.core.database import get_db_session
from src.utils.translation_cache import translation_cache
from src.external.translation_client import translation_client
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class TranslationService:
    """
    Service for handling translation functionality with Google Cloud Translation API.
    """

    def __init__(self):
        self._translate_client = None

    def _get_translate_client(self):
        """Initialize and return Google Cloud Translation client."""
        if self._translate_client is None:
            # Use the project ID and API key from settings
            credentials_info = {
                "type": "service_account",
                "project_id": settings.GOOGLE_CLOUD_PROJECT_ID,
                "private_key_id": "",
                "private_key": "",
                "client_email": "",
                "client_id": "",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": ""
            }

            # If we have an API key, use it
            if settings.GOOGLE_CLOUD_TRANSLATE_API_KEY:
                # For API key authentication, we'll make direct HTTP requests
                pass
            else:
                # For service account authentication
                if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                    self._translate_client = translate.Client()
                else:
                    # Initialize with project ID
                    self._translate_client = translate.Client(
                        project_id=settings.GOOGLE_CLOUD_PROJECT_ID
                    )
        return self._translate_client

    async def translate_content(
        self,
        user_id: str,
        content: str,
        chapter_id: str,
        target_language: str = "ur"
    ) -> dict:
        """
        Translate content to the target language and handle caching.

        Args:
            user_id: ID of the user requesting translation
            content: Content to translate
            chapter_id: ID of the chapter containing the content
            target_language: Target language code (default: 'ur' for Urdu)

        Returns:
            Dictionary with translation result
        """
        # Validate content
        if not content or len(content.strip()) == 0:
            raise ValueError("Content cannot be empty")

        # First, try to get from cache
        cached_translation = await translation_cache.get(
            str(user_id), chapter_id, content
        )

        if cached_translation:
            logger.info(f"Retrieved translation from cache for user {user_id}, chapter {chapter_id}")
            return {
                "translated_content": cached_translation,
                "session_id": str(uuid.uuid4()),  # Using a new ID for this session
                "is_cached": True
            }

        # Perform translation
        translated_content = await self._perform_translation(content, target_language)

        # Store in cache
        await translation_cache.set(
            str(user_id), chapter_id, content, translated_content
        )

        # Create translation session record
        session_id = await self._create_translation_session(
            user_id, content, translated_content, chapter_id
        )

        return {
            "translated_content": translated_content,
            "session_id": session_id,
            "is_cached": False
        }

    async def _perform_translation(self, content: str, target_language: str) -> str:
        """Perform the actual translation using Google Cloud Translation API."""
        try:
            # Use the external translation client
            translated_text = translation_client.translate_text(
                content,
                target_language=target_language,
                source_language="en"
            )

            if translated_text is None:
                logger.warning("Translation API returned None, using fallback")
                # Return original content with error message if translation fails
                return f"Translation failed: {content}"

            return translated_text
        except Exception as e:
            logger.error(f"Translation API error: {str(e)}")
            # Return original content with error message if translation fails
            return f"Translation failed: {content} [Error: {str(e)}]"


    async def _create_translation_session(
        self,
        user_id: str,
        original_content: str,
        translated_content: str,
        chapter_id: str
    ) -> str:
        """Create a translation session record in the database."""
        session_id = uuid.uuid4()

        async with get_db_session() as db:
            # Create new translation session
            translation_session = TranslationSession(
                session_id=session_id,
                user_id=user_id,
                original_content_ref=original_content[:100] + "..." if len(original_content) > 100 else original_content,  # Store a reference, not full content
                translated_content=translated_content,
                chapter_reference=chapter_id,
                translation_timestamp=datetime.utcnow(),
                is_cached=False,
                cache_expires_at=datetime.utcnow() + timedelta(hours=24)
            )

            db.add(translation_session)
            await db.commit()

            return str(session_id)


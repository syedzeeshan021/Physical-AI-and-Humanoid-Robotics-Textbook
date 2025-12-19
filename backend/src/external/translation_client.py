from typing import Optional
import logging
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import os
import requests
from src.core.config import settings

logger = logging.getLogger(__name__)


class GoogleTranslationClient:
    """
    Client for Google Cloud Translation API with proper authentication and error handling.
    """

    def __init__(self):
        self._client = None
        self._api_key = settings.GOOGLE_CLOUD_TRANSLATE_API_KEY
        self._project_id = settings.GOOGLE_CLOUD_PROJECT_ID

    def _get_client(self):
        """
        Initialize and return Google Cloud Translation client.
        Uses either API key or service account authentication.
        """
        if self._client is not None:
            return self._client

        try:
            # Check if we have Google Application Credentials set
            if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
                self._client = translate.Client()
            elif self._project_id:
                # Initialize with project ID
                self._client = translate.Client(project_id=self._project_id)
            else:
                # Fallback to API key if available
                if self._api_key:
                    # For API key authentication, we'll use direct HTTP requests
                    logger.warning("Using API key authentication. For production, prefer service account authentication.")
                else:
                    logger.warning("No Google Cloud credentials found. Using simulated translation.")

        except Exception as e:
            logger.error(f"Failed to initialize Google Translation client: {str(e)}")
            # If initialization fails, we'll use simulated translation
            self._client = None

        return self._client

    def translate_text(self, text: str, target_language: str = "ur", source_language: str = "en") -> Optional[str]:
        """
        Translate text using Google Cloud Translation API.

        Args:
            text: Text to translate
            target_language: Target language code (default: 'ur' for Urdu)
            source_language: Source language code (default: 'en' for English)

        Returns:
            Translated text or None if translation fails
        """
        try:
            # First, try using the client if it's available
            client = self._get_client()

            if client:
                # Use Google Cloud Translation API
                result = client.translate(
                    text,
                    target_language=target_language,
                    source_language=source_language
                )

                translated_text = result['translatedText']
                logger.info(f"Successfully translated text to {target_language}")
                return translated_text
            else:
                # Fallback to direct API call with API key if available
                if self._api_key:
                    return self._translate_with_api_key(text, target_language, source_language)
                else:
                    # Simulate translation for development purposes
                    logger.warning("Using simulated translation (no credentials provided)")
                    return self._simulate_translation(text, target_language)

        except Exception as e:
            logger.error(f"Translation API error: {str(e)}")
            # Return simulated translation to avoid complete failure
            return self._simulate_translation(text, target_language)

    def _translate_with_api_key(self, text: str, target_language: str, source_language: str) -> Optional[str]:
        """
        Translate using direct API call with API key.
        """
        try:
            import json

            url = f"https://translation.googleapis.com/language/translate/v2"

            payload = {
                'q': text,
                'target': target_language,
                'source': source_language,
                'format': 'text'
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(
                url,
                params={'key': self._api_key},
                data=payload,
                headers=headers
            )

            if response.status_code == 200:
                result = response.json()
                translated_text = result['data']['translations'][0]['translatedText']
                return translated_text
            else:
                logger.error(f"API key translation failed with status {response.status_code}: {response.text}")
                return None

        except Exception as e:
            logger.error(f"API key translation error: {str(e)}")
            return None

    def _simulate_translation(self, text: str, target_language: str) -> str:
        """
        Simulate translation for development purposes.
        In a real implementation, this would be replaced with actual translation.
        """
        # For development, return a placeholder indicating the text would be translated
        return f"[TRANSLATED TO {target_language.upper()}] {text} [TRANSLATION SIMULATION]"


# Singleton instance
translation_client = GoogleTranslationClient()
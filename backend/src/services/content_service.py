from typing import Dict, Any, Optional
from openai import OpenAI
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class ContentService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def translate_content(self, content: str, target_language: str = "ur") -> str:
        """
        Translate content to the target language using OpenAI
        """
        try:
            prompt = f"""
            Translate the following text to {target_language}.
            If the target language is 'ur', translate to Urdu.
            Preserve the technical terminology and meaning:

            {content}
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.3
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error translating content: {str(e)}")
            return content  # Return original content if translation fails

    async def personalize_content(self, content: str, user_preferences: Dict[str, Any]) -> str:
        """
        Personalize content based on user preferences
        """
        try:
            software_background = user_preferences.get("software_background", "beginner")
            hardware_background = user_preferences.get("hardware_background", "beginner")

            prompt = f"""
            Personalize the following content based on the user's background:
            - Software background: {software_background}
            - Hardware background: {hardware_background}

            Make the content more relevant and understandable for this user profile.
            If they have beginner background, add more explanations.
            If they have advanced background, add more technical depth.

            Original content:
            {content}
            """

            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.5
            )

            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error personalizing content: {str(e)}")
            return content  # Return original content if personalization fails

# Global instance
content_service = ContentService()
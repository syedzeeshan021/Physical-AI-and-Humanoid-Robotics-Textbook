from typing import Dict, List, Optional
import openai
from src.core.config import settings


class TranslationService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    async def translate_text(self, text: str, target_language: str = "ur") -> str:
        """
        Translate text to the target language
        """
        if target_language.lower() == "en":
            return text  # No translation needed

        try:
            # Create a prompt for translation
            prompt = f"""
            Translate the following text to {self.get_language_name(target_language)}.
            Only return the translated text, nothing else.

            Text to translate: {text}
            """

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.3
            )

            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            # If translation fails, return the original text
            return text

    async def translate_chapter_content(self, content: str, target_language: str = "ur") -> str:
        """
        Translate chapter content to the target language
        """
        # For simplicity, we're translating the entire content
        # In a production system, we might want to break it into smaller chunks
        return await self.translate_text(content, target_language)

    def get_language_name(self, language_code: str) -> str:
        """
        Get the full language name from the code
        """
        language_map = {
            "ur": "Urdu",
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ar": "Arabic",
        }
        return language_map.get(language_code.lower(), language_code)


# Global instance
translation_service = TranslationService()
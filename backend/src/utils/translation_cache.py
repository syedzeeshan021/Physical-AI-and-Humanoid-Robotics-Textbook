import asyncio
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import hashlib
import json

from src.models.translation_session import TranslationSession


class TranslationCache:
    """
    In-memory cache for translated content with 24-hour TTL.
    """

    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    def _generate_cache_key(self, user_id: str, chapter_id: str, content_hash: str) -> str:
        """Generate a unique cache key based on user, chapter, and content."""
        return f"{user_id}:{chapter_id}:{content_hash}"

    def _is_expired(self, expires_at: datetime) -> bool:
        """Check if cache entry has expired."""
        return datetime.utcnow() > expires_at

    async def get(self, user_id: str, chapter_id: str, content: str) -> Optional[str]:
        """
        Get cached translation if it exists and hasn't expired.

        Args:
            user_id: The ID of the user requesting translation
            chapter_id: The ID of the chapter being translated
            content: The original content to be translated

        Returns:
            Cached translated content if available and not expired, None otherwise
        """
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        cache_key = self._generate_cache_key(user_id, chapter_id, content_hash)

        async with self._lock:
            if cache_key in self._cache:
                entry = self._cache[cache_key]
                if not self._is_expired(entry["expires_at"]):
                    return entry["translated_content"]
                else:
                    # Remove expired entry
                    del self._cache[cache_key]

        return None

    async def set(self, user_id: str, chapter_id: str, original_content: str,
                  translated_content: str, ttl_hours: int = 24) -> None:
        """
        Store a translation in cache with TTL.

        Args:
            user_id: The ID of the user requesting translation
            chapter_id: The ID of the chapter being translated
            original_content: The original content
            translated_content: The translated content
            ttl_hours: Time-to-live in hours (default 24 hours)
        """
        content_hash = hashlib.sha256(original_content.encode()).hexdigest()
        cache_key = self._generate_cache_key(user_id, chapter_id, content_hash)

        expires_at = datetime.utcnow() + timedelta(hours=ttl_hours)

        async with self._lock:
            self._cache[cache_key] = {
                "original_content": original_content,
                "translated_content": translated_content,
                "expires_at": expires_at,
                "created_at": datetime.utcnow()
            }

    async def invalidate(self, user_id: str, chapter_id: str, content: str) -> bool:
        """
        Invalidate a specific cache entry.

        Args:
            user_id: The ID of the user
            chapter_id: The ID of the chapter
            content: The original content

        Returns:
            True if entry was found and removed, False otherwise
        """
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        cache_key = self._generate_cache_key(user_id, chapter_id, content_hash)

        async with self._lock:
            if cache_key in self._cache:
                del self._cache[cache_key]
                return True
            return False

    async def cleanup_expired(self) -> int:
        """
        Remove all expired cache entries.

        Returns:
            Number of entries removed
        """
        current_time = datetime.utcnow()
        to_remove = []

        async with self._lock:
            for key, entry in self._cache.items():
                if self._is_expired(entry["expires_at"]):
                    to_remove.append(key)

            for key in to_remove:
                del self._cache[key]

            return len(to_remove)


# Global instance of the cache
translation_cache = TranslationCache()
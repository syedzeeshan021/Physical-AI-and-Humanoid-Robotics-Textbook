import asyncio
import time
from typing import Any, Optional
from collections import OrderedDict


class SimpleCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Initialize cache with max size and time-to-live (in seconds)
        """
        self.max_size = max_size
        self.ttl = ttl
        self._cache = OrderedDict()
        self._timestamps = {}

    def _is_expired(self, key: str) -> bool:
        """
        Check if a cache entry is expired
        """
        if key not in self._timestamps:
            return True
        return time.time() - self._timestamps[key] > self.ttl

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        """
        if key not in self._cache or self._is_expired(key):
            if key in self._cache:
                del self._cache[key]
                del self._timestamps[key]
            return None

        # Move to end to show recent usage
        value = self._cache.pop(key)
        self._cache[key] = value
        return value

    def set(self, key: str, value: Any):
        """
        Set value in cache
        """
        # If key already exists, update it
        if key in self._cache:
            self._cache.pop(key)
        elif len(self._cache) >= self.max_size:
            # Remove oldest item
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            del self._timestamps[oldest_key]

        self._cache[key] = value
        self._timestamps[key] = time.time()

    def delete(self, key: str):
        """
        Delete value from cache
        """
        if key in self._cache:
            del self._cache[key]
            del self._timestamps[key]

    def clear(self):
        """
        Clear all cache
        """
        self._cache.clear()
        self._timestamps.clear()

    def size(self) -> int:
        """
        Get current cache size
        """
        return len(self._cache)


# Global cache instances for different use cases
rag_cache = SimpleCache(max_size=500, ttl=1800)  # 500 items, 30 minutes TTL for RAG queries
chapter_cache = SimpleCache(max_size=200, ttl=3600)  # 200 items, 1 hour TTL for chapters
user_cache = SimpleCache(max_size=100, ttl=900)  # 100 items, 15 minutes TTL for user data
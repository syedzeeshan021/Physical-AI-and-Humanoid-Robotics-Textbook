import time
from typing import Dict
from collections import defaultdict
from src.core.config import settings


class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)  # IP -> list of request timestamps
        self.window = settings.RATE_LIMIT_WINDOW  # Time window in seconds
        self.max_requests = settings.RATE_LIMIT_REQUESTS  # Max requests per window

    def is_allowed(self, identifier: str = "default") -> bool:
        """
        Check if a request from the given identifier is allowed
        """
        now = time.time()
        # Clean old requests outside the time window
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < self.window
        ]

        # Check if we're under the limit
        if len(self.requests[identifier]) < self.max_requests:
            self.requests[identifier].append(now)
            return True

        return False

    def get_reset_time(self, identifier: str = "default") -> int:
        """
        Get the time when the rate limit will reset for this identifier
        """
        if not self.requests[identifier]:
            return 0

        # Find the earliest request in the window
        oldest_request = min(self.requests[identifier])
        return int(oldest_request + self.window)


# Global rate limiter instance
rate_limiter = RateLimiter()
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from src.utils.rate_limit import rate_limiter


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Skip rate limiting for health checks and static files
        if request.url.path in ["/health", "/docs", "/redoc"] or request.url.path.startswith("/static"):
            return await call_next(request)

        # Get client IP for rate limiting
        client_ip = request.client.host

        # Check rate limit
        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )

        response = await call_next(request)
        return response
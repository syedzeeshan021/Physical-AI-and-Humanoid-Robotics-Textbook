from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.api import router
from src.core.config import settings
from src.core.error_handlers import setup_error_handlers
from src.middleware.rate_limit import RateLimitMiddleware
from src.core.logging import setup_logging

# Setup logging
setup_logging()

# Create a limiter instance
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Textbook Generation API with RAG Chatbot"
)

# Setup error handlers
setup_error_handlers(app)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)

# Add slowapi rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Textbook Generation API"}

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "textbook-generation-api",
        "version": settings.VERSION,
        "checks": {
            "database": "not checked",
            "vector_store": "not checked",
            "external_apis": "not checked"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
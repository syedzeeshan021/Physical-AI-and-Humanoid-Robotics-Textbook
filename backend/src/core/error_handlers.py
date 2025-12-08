from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import logging
import traceback
from contextlib import asynccontextmanager


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Global HTTP exception handler
    """
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Global general exception handler
    """
    logger.error(f"Unhandled Exception: {str(exc)}")
    logger.error(traceback.format_exc())

    # In production, you might not want to return the full traceback
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


def setup_error_handlers(app):
    """
    Setup error handlers for the FastAPI app
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
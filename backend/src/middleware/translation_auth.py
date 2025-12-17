from fastapi import HTTPException, status
from jose import JWTError, jwt
import logging
from sqlalchemy import select, func

from src.core.config import settings
from src.models.user import User
from src.core.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


class TranslationAuthMiddleware:
    """
    Middleware to verify user authentication status for translation feature.
    Checks that user has basic account registration (auth_status is not 'unverified').
    """

    def __init__(self):
        pass

    async def verify_translation_access(self, token: str) -> User:
        """
        Verify that the user has proper authentication status for translation access.
        Only users with auth_status 'verified' or 'active' can access translation.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials for translation access",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        # Get user from database
        async with get_db_session() as db:
            result = await db.execute(select(User).filter(User.email == email))
            user = result.scalar_one_or_none()

            if user is None:
                raise credentials_exception

            # Check if user has proper authentication status for translation
            if user.auth_status == 'unverified':
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Account must be verified to access translation feature"
                )

            return user


# Create an instance of the middleware
translation_auth = TranslationAuthMiddleware()
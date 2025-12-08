from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.core.database import AsyncSessionLocal


class UserService:
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """
        Get a user by their email
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            return user

    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Get a user by their ID
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            return user

    @staticmethod
    async def create_user(email: str, hashed_password: str) -> User:
        """
        Create a new user
        """
        async with AsyncSessionLocal() as session:
            user = User(
                email=email,
                hashed_password=hashed_password
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def update_user_preferences(user_id: str, preferences: dict) -> User:
        """
        Update user preferences
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise ValueError(f"User with id {user_id} not found")

            user.preferences = preferences
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def update_user_progress(user_id: str, progress: dict) -> User:
        """
        Update user progress
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()

            if not user:
                raise ValueError(f"User with id {user_id} not found")

            user.progress = progress
            await session.commit()
            await session.refresh(user)
            return user


# Global instance
user_service = UserService()
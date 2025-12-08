from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.chat_session import ChatSession
from src.models.chat_message import ChatMessage
from src.core.database import AsyncSessionLocal


class ChatService:
    @staticmethod
    async def create_session(user_id: str = None) -> ChatSession:
        """
        Create a new chat session
        """
        async with AsyncSessionLocal() as session:
            chat_session = ChatSession(user_id=user_id)
            session.add(chat_session)
            await session.commit()
            await session.refresh(chat_session)
            return chat_session

    @staticmethod
    async def get_session_by_id(session_id: str) -> Optional[ChatSession]:
        """
        Get a chat session by ID
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatSession).where(ChatSession.id == session_id)
            )
            chat_session = result.scalar_one_or_none()
            return chat_session

    @staticmethod
    async def add_message_to_session(session_id: str, role: str, content: str) -> ChatMessage:
        """
        Add a message to a chat session
        """
        async with AsyncSessionLocal() as session:
            chat_message = ChatMessage(
                session_id=session_id,
                role=role,
                content=content
            )
            session.add(chat_message)
            await session.commit()
            await session.refresh(chat_message)
            return chat_message

    @staticmethod
    async def get_messages_by_session(session_id: str) -> List[ChatMessage]:
        """
        Get all messages for a chat session
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(ChatMessage)
                .where(ChatMessage.session_id == session_id)
                .order_by(ChatMessage.created_at)
            )
            messages = result.scalars().all()
            return messages


# Global instance
chat_service = ChatService()
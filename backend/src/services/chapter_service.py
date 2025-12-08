from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.chapter import Chapter
from src.core.database import AsyncSessionLocal


class ChapterService:
    @staticmethod
    async def get_all_chapters() -> List[Chapter]:
        """
        Get all chapters from the database
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Chapter).order_by(Chapter.order))
            chapters = result.scalars().all()
            return chapters

    @staticmethod
    async def get_chapter_by_id(chapter_id: str) -> Optional[Chapter]:
        """
        Get a specific chapter by ID
        """
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Chapter).where(Chapter.id == chapter_id)
            )
            chapter = result.scalar_one_or_none()
            return chapter

    @staticmethod
    async def create_chapter(title: str, content: str, order: int, word_count: int) -> Chapter:
        """
        Create a new chapter
        """
        async with AsyncSessionLocal() as session:
            chapter = Chapter(
                title=title,
                content=content,
                order=order,
                word_count=word_count
            )
            session.add(chapter)
            await session.commit()
            await session.refresh(chapter)
            return chapter
from fastapi import APIRouter, HTTPException
from typing import List
from src.models.chapter import Chapter
from src.services.chapter_service import ChapterService
from src.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[dict])
async def get_chapters():
    """
    Get all textbook chapters
    """
    try:
        chapters = await ChapterService.get_all_chapters()
        return [
            {
                "id": str(chapter.id),
                "title": chapter.title,
                "order": chapter.order,
                "word_count": chapter.word_count
            }
            for chapter in chapters
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{chapter_id}", response_model=dict)
async def get_chapter(chapter_id: str):
    """
    Get specific chapter content
    """
    try:
        chapter = await ChapterService.get_chapter_by_id(chapter_id)
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        return {
            "id": str(chapter.id),
            "title": chapter.title,
            "content": chapter.content,
            "order": chapter.order
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter

from src.api import chapters, rag, auth, users

router = APIRouter()
router.include_router(chapters.router, prefix="/chapters", tags=["chapters"])
router.include_router(rag.router, prefix="/rag", tags=["rag"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
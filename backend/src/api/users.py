from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from src.services.user_service import UserService
from src.auth.utils import verify_token
from src.core.config import settings
from src.models.user import User
from src.auth.auth_service import get_current_user

router = APIRouter()


def get_current_user_id(token: str = None) -> str:
    """
    Get current user ID from token or return None for anonymous access
    """
    if not token:
        return None  # Anonymous user

    payload = verify_token(token.replace("Bearer ", ""))
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id


@router.get("/preferences")
async def get_user_preferences(token: str = None):
    """
    Get user preferences
    """
    user_id = get_current_user_id(token)

    if not user_id:
        # Return default preferences for anonymous users
        return {
            "language": "en",
            "theme": "light",
            "personalization_enabled": False
        }

    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.preferences or {
        "language": "en",
        "theme": "light",
        "personalization_enabled": True
    }


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information
    """
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return user information (excluding sensitive data like hashed_password)
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "auth_status": current_user.auth_status,
        "preferences": current_user.preferences,
        "progress": current_user.progress,
        "created_at": current_user.created_at,
        "updated_at": current_user.updated_at
    }


@router.put("/preferences")
async def update_user_preferences(preferences: Dict[str, Any], token: str = None):
    """
    Update user preferences
    """
    user_id = get_current_user_id(token)

    if not user_id:
        # For anonymous users, we can't save preferences, so just return them
        return preferences

    user = await UserService.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await UserService.update_user_preferences(user_id, preferences)
    return updated_user.preferences
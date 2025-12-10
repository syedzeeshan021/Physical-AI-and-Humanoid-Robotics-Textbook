from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_service import (
    Token, UserCreate, authenticate_user, create_access_token,
    get_password_hash, get_user_by_email
)
from src.core.database import get_db_session
from src.models.user import User
from src.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
async def register_user(user_create: UserCreate, db: AsyncSession = Depends(get_db_session)):
    """Register a new user with background information"""
    # Check if user already exists
    existing_user = await get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create user preferences based on background information
    preferences = {
        "software_background": user_create.software_background,
        "hardware_background": user_create.hardware_background,
        "language_preference": "en",  # Default language
        "personalization_enabled": True
    }

    # Create new user
    db_user = User(
        email=user_create.email,
        hashed_password=hashed_password,
        preferences=preferences,
        progress={}  # Empty progress initially
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session)
):
    """Login endpoint that returns an access token"""
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
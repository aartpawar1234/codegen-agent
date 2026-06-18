"""
FastAPI routers for login, logout, and refresh endpoints.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas import Token, UserCreate, UserLogin, UserResponse
from src.crud import get_user_by_email, create_user, is_token_blacklisted
from src.auth import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_token,
)
from src.config import settings
from src.utils import revoke_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db),
    request: Request = None,
):
    """
    Authenticate a user and return JWT tokens.

    Args:
        login_data: User login credentials
        db: Database session
        request: FastAPI request object for rate limiting

    Returns:
        Token containing access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid or user is inactive
    """
    # Rate limiting check (simplified - in production use Redis)
    # This is a placeholder for actual rate limiting implementation

    # Get user from database
    user = get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is inactive",
        )

    # Create tokens
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires,
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    Revoke a refresh token to logout the user.

    Args:
        refresh_token: Refresh token to revoke
        db: Database session

    Returns:
        Success message

    Raises:
        HTTPException: If token is already revoked
    """
    # Check if token is already blacklisted
    if is_token_blacklisted(db, refresh_token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already revoked",
        )

    # Revoke the token
    revoke_token(refresh_token, db)

    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token)
async def refresh(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    """
    Refresh an access token using a valid refresh token.

    Args:
        refresh_token: Valid refresh token
        db: Database session

    Returns:
        New token pair with access and refresh tokens

    Raises:
        HTTPException: If refresh token is invalid or revoked
    """
    # Check if token is blacklisted
    if is_token_blacklisted(db, refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked",
        )

    # Verify token
    token_data = verify_token(refresh_token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Get user
    user = get_user_by_email(db, token_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Create new tokens
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.email},
        expires_delta=refresh_token_expires,
    )

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user information

    Raises:
        HTTPException: If user already exists
    """
    # Check if user already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password and create user
    hashed_password = get_password_hash(user_data.password)
    user = create_user(db, user_data, hashed_password)

    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        created_at=user.created_at,
    )

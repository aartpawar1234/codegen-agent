from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth.crud import (
    create_refresh_token_record,
    get_user_by_email,
    revoke_refresh_token_record,
)
from src.auth.dependencies import get_current_user, get_refresh_token
from src.auth.exceptions import InvalidCredentialsError, TokenRevokedError
from src.auth.schemas import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse
from src.auth.utils import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_jwt_secret,
)
from src.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(login_request: LoginRequest):
    """Login endpoint to authenticate user and return JWT tokens."""
    user = get_user_by_email(login_request.email)
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise InvalidCredentialsError()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(user.id, access_token_expires)
    refresh_token = create_refresh_token(user.id, refresh_token_expires)

    create_refresh_token_record(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + refresh_token_expires,
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(refresh_token: str = Depends(get_refresh_token)):
    """Logout endpoint to revoke refresh token."""
    revoke_refresh_token_record(refresh_token)
    return None

@router.post("/refresh", response_model=RefreshResponse)
async def refresh(refresh_request: RefreshRequest):
    """Refresh endpoint to issue new access token."""
    try:
        payload = verify_token(refresh_request.refresh_token)
        if payload.get("type") != "refresh":
            raise TokenRevokedError()
        if is_refresh_token_revoked(refresh_request.refresh_token):
            raise TokenRevokedError()

        user_id = payload.get("sub")
        if not user_id:
            raise TokenRevokedError()

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(user_id, access_token_expires)

        return RefreshResponse(
            access_token=access_token,
            token_type="bearer",
        )
    except Exception as e:
        raise TokenRevokedError()
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.auth.crud import get_user_by_email, is_refresh_token_revoked
from src.auth.exceptions import InvalidCredentialsError, TokenRevokedError
from src.auth.models import User
from src.auth.schemas import LoginRequest
from src.auth.utils import verify_token, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Dependency to get the current authenticated user."""
    try:
        payload = verify_token(token)
        if payload.get("type") != "access":
            raise InvalidCredentialsError()
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidCredentialsError()
        user = get_user_by_email(user_id)
        if not user:
            raise InvalidCredentialsError()
        return user
    except Exception as e:
        raise InvalidCredentialsError()

async def get_refresh_token(token: str) -> str:
    """Dependency to validate refresh token."""
    try:
        payload = verify_token(token)
        if payload.get("type") != "refresh":
            raise TokenRevokedError()
        if is_refresh_token_revoked(token):
            raise TokenRevokedError()
        return token
    except Exception as e:
        raise TokenRevokedError()
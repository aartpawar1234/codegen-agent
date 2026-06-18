from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from src.auth.models import User, RefreshToken
from src.auth.exceptions import TokenRevokedError, TokenExpiredError
from src.auth.schemas import LoginResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"sub": user_id, "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(to_encode, str(get_jwt_secret()), algorithm="HS256")
    return encoded_jwt

def create_refresh_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT refresh token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode = {"sub": user_id, "exp": expire, "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, str(get_jwt_secret()), algorithm="HS256")
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify a JWT token and return its payload."""
    try:
        payload = jwt.decode(token, str(get_jwt_secret()), algorithms=["HS256"])
        return payload
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except InvalidTokenError:
        raise TokenExpiredError()

def revoke_refresh_token(refresh_token: RefreshToken) -> None:
    """Revoke a refresh token."""
    refresh_token.revoked = True

def get_jwt_secret() -> str:
    """Get JWT secret from environment variables."""
    import os
    secret = os.getenv("JWT_SECRET")
    if not secret:
        raise ValueError("JWT_SECRET environment variable not set")
    return secret
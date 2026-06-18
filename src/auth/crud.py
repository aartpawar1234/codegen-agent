from datetime import datetime, timedelta
from typing import Optional
from uuid import uuid4
from src.auth.models import User, RefreshToken
from src.auth.exceptions import InvalidCredentialsError
from src.auth.schemas import LoginResponse
from src.auth.utils import get_password_hash, verify_password, create_refresh_token

def get_user_by_email(email: str) -> Optional[User]:
    """Get a user by email."""
    from src.database import SessionLocal
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def create_refresh_token_record(user_id: str, token: str, expires_at: datetime) -> RefreshToken:
    """Create a refresh token record in the database."""
    from src.database import SessionLocal
    db = SessionLocal()
    try:
        refresh_token = RefreshToken(
            id=str(uuid4()),
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token
    finally:
        db.close()

def revoke_refresh_token_record(token: str) -> None:
    """Revoke a refresh token record in the database."""
    from src.database import SessionLocal
    db = SessionLocal()
    try:
        refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        if refresh_token:
            refresh_token.revoked = True
            db.commit()
    finally:
        db.close()

def is_refresh_token_revoked(token: str) -> bool:
    """Check if a refresh token is revoked."""
    from src.database import SessionLocal
    db = SessionLocal()
    try:
        refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
        return refresh_token.revoked if refresh_token else True
    finally:
        db.close()
"""
Database CRUD operations for User and TokenBlacklist.
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models import User, TokenBlacklist
from src.schemas import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    """Get a user by email address."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    """Create a new user in the database."""
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def blacklist_token(db: Session, token: str, expires_at: datetime) -> TokenBlacklist:
    """Add a token to the blacklist."""
    db_token = TokenBlacklist(token=token, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def is_token_blacklisted(db: Session, token: str) -> bool:
    """Check if a token is blacklisted."""
    blacklisted_token = db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first()
    if blacklisted_token:
        # Check if token has expired
        if blacklisted_token.expires_at < datetime.now(timezone.utc):
            db.delete(blacklisted_token)
            db.commit()
            return False
        return True
    return False

"""
Utility functions for JWT token handling and blacklisting.
"""

from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.config import settings
from src.crud import is_token_blacklisted
from src.database import get_db
from src.schemas import TokenData
from src.auth import verify_token

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def decode_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    """
    Decode and verify a JWT token.

    Args:
        token: JWT token from Authorization header

    Returns:
        TokenData containing user email

    Raises:
        HTTPException: If token is invalid or expired
    """
    db = next(get_db())
    try:
        # Check if token is blacklisted
        if is_token_blacklisted(db, token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token_data = verify_token(token)
        if token_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data
    finally:
        db.close()


def revoke_token(token: str, db: Session) -> None:
    """
    Revoke a refresh token by adding it to the blacklist.

    Args:
        token: Refresh token to revoke
        db: Database session

    Raises:
        HTTPException: If token is already blacklisted
    """
    # Check if token is already blacklisted
    if is_token_blacklisted(db, token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token already revoked",
        )

    # Calculate expiration time (same as refresh token expiration)
    expires_at = datetime.now(timezone.utc) + timezone.timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )

    # Add to blacklist
    from src.crud import blacklist_token

    blacklist_token(db, token, expires_at)

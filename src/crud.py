from sqlalchemy.orm import Session
from .models import User, TokenBlacklist


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create_token(db: Session, token: str) -> TokenBlacklist:
    db_token = TokenBlacklist(token=token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def revoke_token(db: Session, token: str):
    db.query(TokenBlacklist).filter(TokenBlacklist.token == token).delete()
    db.commit()


def is_token_revoked(db: Session, token: str) -> bool:
    return db.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None
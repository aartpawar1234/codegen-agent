from sqlalchemy.orm import Session
from .models import User
from .schemas.auth import UserCreate
from sqlalchemy.exc import IntegrityError
from ..utils.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")
    return db_user

from sqlalchemy.orm import Session
from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserLogin


def register_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and user.hashed_password == password:
        return user
    return None


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
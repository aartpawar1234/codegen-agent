import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.crud import get_user_by_email, create_token, revoke_token, is_token_revoked
from src.models import User, TokenBlacklist

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_user_by_email(setup_database):
    db = TestingSessionLocal()
    user = User(email="test@example.com", hashed_password="hashedpassword")
    db.add(user)
    db.commit()
    db.refresh(user)
    retrieved_user = get_user_by_email(db, "test@example.com")
    assert retrieved_user.email == user.email


def test_create_token(setup_database):
    db = TestingSessionLocal()
    token = "some_token"
    created_token = create_token(db, token)
    assert created_token.token == token


def test_revoke_token(setup_database):
    db = TestingSessionLocal()
    token = "some_token"
    create_token(db, token)
    revoke_token(db, token)
    assert is_token_revoked(db, token) is True
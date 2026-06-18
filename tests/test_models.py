from src.auth.models import User, RefreshToken, Base
from sqlalchemy import create_engine, Column, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
import pytest


@pytest.fixture
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def session(engine):
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def test_user_model():
    """Test User model has correct attributes."""
    user = User(
        id="user123",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    
    assert user.id == "user123"
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.is_active is True
    assert user.created_at is not None
    assert user.updated_at is not None


def test_refresh_token_model():
    """Test RefreshToken model has correct attributes."""
    from datetime import datetime
    refresh_token = RefreshToken(
        id="token123",
        user_id="user123",
        token="refresh_token_123",
        expires_at=datetime.utcnow(),
        revoked=False
    )
    
    assert refresh_token.id == "token123"
    assert refresh_token.user_id == "user123"
    assert refresh_token.token == "refresh_token_123"
    assert refresh_token.expires_at is not None
    assert refresh_token.revoked is False
    assert refresh_token.created_at is not None
    assert refresh_token.updated_at is not None


def test_user_model_persistence(session):
    """Test User model can be persisted to database."""
    user = User(
        id="user123",
        email="test@example.com",
        hashed_password="hashed_password"
    )
    session.add(user)
    session.commit()
    
    retrieved_user = session.query(User).filter(User.id == "user123").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"


def test_refresh_token_model_persistence(session):
    """Test RefreshToken model can be persisted to database."""
    from datetime import datetime
    refresh_token = RefreshToken(
        id="token123",
        user_id="user123",
        token="refresh_token_123",
        expires_at=datetime.utcnow(),
        revoked=False
    )
    session.add(refresh_token)
    session.commit()
    
    retrieved_token = session.query(RefreshToken).filter(RefreshToken.id == "token123").first()
    assert retrieved_token is not None
    assert retrieved_token.token == "refresh_token_123"
    assert retrieved_token.revoked is False
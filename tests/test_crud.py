import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.auth.crud import (
    get_user_by_email,
    create_refresh_token_record,
    revoke_refresh_token_record,
    is_refresh_token_revoked
)
from src.auth.models import User, RefreshToken
from src.auth.exceptions import InvalidCredentialsError


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_user():
    return User(
        id="user123",
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True
    )


@pytest.fixture
def mock_refresh_token():
    return RefreshToken(
        id="token123",
        user_id="user123",
        token="refresh_token_123",
        expires_at=datetime.utcnow() + timedelta(days=7),
        revoked=False
    )


def test_get_user_by_email_found(mock_db, mock_user):
    """Test get_user_by_email returns user when found."""
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    result = get_user_by_email(mock_db, "test@example.com")
    assert result == mock_user
    mock_db.query.assert_called_once()


def test_get_user_by_email_not_found(mock_db):
    """Test get_user_by_email returns None when user not found."""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    result = get_user_by_email(mock_db, "nonexistent@example.com")
    assert result is None


def test_create_refresh_token_record(mock_db, mock_refresh_token):
    """Test create_refresh_token_record creates and returns a refresh token."""
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    expires_at = datetime.utcnow() + timedelta(days=7)
    result = create_refresh_token_record(
        mock_db,
        "user123",
        "refresh_token_123",
        expires_at
    )
    
    assert result.user_id == "user123"
    assert result.token == "refresh_token_123"
    assert result.expires_at == expires_at
    assert result.revoked is False
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_revoke_refresh_token_record_found(mock_db, mock_refresh_token):
    """Test revoke_refresh_token_record revokes an existing token."""
    mock_db.query.return_value.filter.return_value.first.return_value = mock_refresh_token
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = None
    
    result = revoke_refresh_token_record(mock_db, "refresh_token_123")
    
    assert result.revoked is True
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()


def test_revoke_refresh_token_record_not_found(mock_db):
    """Test revoke_refresh_token_record raises InvalidCredentialsError when token not found."""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    with pytest.raises(InvalidCredentialsError):
        revoke_refresh_token_record(mock_db, "nonexistent_token")


def test_is_refresh_token_revoked_true(mock_db, mock_refresh_token):
    """Test is_refresh_token_revoked returns True when token is revoked."""
    mock_refresh_token.revoked = True
    mock_db.query.return_value.filter.return_value.first.return_value = mock_refresh_token
    
    result = is_refresh_token_revoked(mock_db, "refresh_token_123")
    assert result is True


def test_is_refresh_token_revoked_false(mock_db, mock_refresh_token):
    """Test is_refresh_token_revoked returns False when token is not revoked."""
    mock_refresh_token.revoked = False
    mock_db.query.return_value.filter.return_value.first.return_value = mock_refresh_token
    
    result = is_refresh_token_revoked(mock_db, "refresh_token_123")
    assert result is False


def test_is_refresh_token_revoked_not_found(mock_db):
    """Test is_refresh_token_revoked returns True when token not found."""
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    result = is_refresh_token_revoked(mock_db, "nonexistent_token")
    assert result is True
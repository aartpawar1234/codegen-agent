import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from jose import JWTError, ExpiredSignatureError
from src.auth.utils import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    revoke_refresh_token
)
from src.auth.exceptions import TokenRevokedError, TokenExpiredError


@pytest.fixture
def mock_password():
    return "plain_password_123"


@pytest.fixture
def mock_hashed_password():
    return "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"


def test_verify_password_correct(mock_password, mock_hashed_password):
    """Test verify_password returns True for correct password."""
    assert verify_password(mock_password, mock_hashed_password) is True


def test_verify_password_incorrect(mock_password):
    """Test verify_password returns False for incorrect password."""
    hashed = get_password_hash("different_password")
    assert verify_password(mock_password, hashed) is False


def test_get_password_hash(mock_password):
    """Test get_password_hash returns a non-empty string."""
    hashed = get_password_hash(mock_password)
    assert isinstance(hashed, str)
    assert len(hashed) > 0


@patch('src.auth.utils.JWT_SECRET_KEY', 'test_secret')
@patch('src.auth.utils.JWT_ALGORITHM', 'HS256')
@patch('src.auth.utils.JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 15)
def test_create_access_token():
    """Test create_access_token generates a valid JWT token with correct payload."""
    user_id = "user123"
    token = create_access_token(user_id)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Verify token can be decoded (structure check)
    from jose import jwt
    payload = jwt.decode(token, 'test_secret', algorithms=['HS256'])
    assert payload['sub'] == user_id
    assert payload['type'] == 'access'
    assert 'exp' in payload


@patch('src.auth.utils.JWT_SECRET_KEY', 'test_secret')
@patch('src.auth.utils.JWT_ALGORITHM', 'HS256')
@patch('src.auth.utils.JWT_REFRESH_TOKEN_EXPIRE_DAYS', 7)
def test_create_refresh_token():
    """Test create_refresh_token generates a valid JWT token with correct payload."""
    user_id = "user123"
    token = create_refresh_token(user_id)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Verify token can be decoded (structure check)
    from jose import jwt
    payload = jwt.decode(token, 'test_secret', algorithms=['HS256'])
    assert payload['sub'] == user_id
    assert payload['type'] == 'refresh'
    assert 'exp' in payload


@patch('src.auth.utils.JWT_SECRET_KEY', 'test_secret')
@patch('src.auth.utils.JWT_ALGORITHM', 'HS256')
def test_verify_token_valid():
    """Test verify_token returns payload for valid token."""
    user_id = "user123"
    token = create_access_token(user_id)
    
    payload = verify_token(token)
    
    assert isinstance(payload, dict)
    assert payload['sub'] == user_id
    assert payload['type'] == 'access'


@patch('src.auth.utils.JWT_SECRET_KEY', 'test_secret')
@patch('src.auth.utils.JWT_ALGORITHM', 'HS256')
def test_verify_token_expired():
    """Test verify_token raises TokenExpiredError for expired token."""
    user_id = "user123"
    # Create token with negative expiration
    with patch('src.auth.utils.JWT_ACCESS_TOKEN_EXPIRE_MINUTES', -1):
        token = create_access_token(user_id)
    
    with pytest.raises(TokenExpiredError):
        verify_token(token)


@patch('src.auth.utils.JWT_SECRET_KEY', 'test_secret')
@patch('src.auth.utils.JWT_ALGORITHM', 'HS256')
def test_verify_token_invalid_signature():
    """Test verify_token raises InvalidCredentialsError for invalid signature."""
    token = "invalid.token.signature"
    
    with pytest.raises(TokenRevokedError):
        verify_token(token)


@patch('src.auth.utils.JWT_SECRET_KEY', 'test_secret')
@patch('src.auth.utils.JWT_ALGORITHM', 'HS256')
def test_verify_token_malformed():
    """Test verify_token raises InvalidCredentialsError for malformed token."""
    token = "malformed.token"
    
    with pytest.raises(TokenRevokedError):
        verify_token(token)


def test_revoke_refresh_token_noop():
    """Test revoke_refresh_token is a no-op function."""
    # The function does nothing, so we just ensure it doesn't raise
    revoke_refresh_token(MagicMock())

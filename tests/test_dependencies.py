import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.auth.dependencies import get_current_user, get_refresh_token
from src.auth.schemas import TokenData
from src.auth.exceptions import InvalidCredentialsError, TokenRevokedError, TokenExpiredError
from src.auth.utils import verify_token


@pytest.fixture
def mock_db():
    return MagicMock(spec=Session)


@pytest.fixture
def mock_token():
    return "valid_token"


@pytest.fixture
def mock_token_data():
    return TokenData(user_id="user123", email="test@example.com")


@pytest.mark.asyncio
async def test_get_current_user_valid_token(mock_db, mock_token, mock_token_data):
    """Test get_current_user returns TokenData for valid token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify:
        mock_verify.return_value = mock_token_data
        
        result = await get_current_user(mock_token, mock_db)
        
        assert result == mock_token_data
        mock_verify.assert_called_once_with(mock_token)


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(mock_db, mock_token):
    """Test get_current_user raises HTTPException for invalid token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify:
        mock_verify.side_effect = InvalidCredentialsError()
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_token, mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_revoked_token(mock_db, mock_token):
    """Test get_current_user raises HTTPException for revoked token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify:
        mock_verify.side_effect = TokenRevokedError()
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_token, mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token has been revoked" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_current_user_expired_token(mock_db, mock_token):
    """Test get_current_user raises HTTPException for expired token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify:
        mock_verify.side_effect = TokenExpiredError()
        
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(mock_token, mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token has expired" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_refresh_token_valid_token(mock_db, mock_token, mock_token_data):
    """Test get_refresh_token returns TokenData for valid refresh token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify, \
         patch('src.auth.dependencies.is_refresh_token_revoked') as mock_revoked:
        mock_verify.return_value = mock_token_data
        mock_revoked.return_value = False
        
        result = await get_refresh_token(mock_token, mock_db)
        
        assert result == mock_token_data
        mock_verify.assert_called_once_with(mock_token)
        mock_revoked.assert_called_once_with(mock_db, mock_token)


@pytest.mark.asyncio
async def test_get_refresh_token_revoked_token(mock_db, mock_token):
    """Test get_refresh_token raises HTTPException for revoked token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify, \
         patch('src.auth.dependencies.is_refresh_token_revoked') as mock_revoked:
        mock_verify.return_value = TokenData(user_id="user123")
        mock_revoked.return_value = True
        
        with pytest.raises(HTTPException) as exc_info:
            await get_refresh_token(mock_token, mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token has been revoked" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_refresh_token_invalid_token(mock_db, mock_token):
    """Test get_refresh_token raises HTTPException for invalid token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify:
        mock_verify.side_effect = InvalidCredentialsError()
        
        with pytest.raises(HTTPException) as exc_info:
            await get_refresh_token(mock_token, mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid credentials" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_refresh_token_expired_token(mock_db, mock_token):
    """Test get_refresh_token raises HTTPException for expired token."""
    with patch('src.auth.dependencies.verify_token') as mock_verify:
        mock_verify.side_effect = TokenExpiredError()
        
        with pytest.raises(HTTPException) as exc_info:
            await get_refresh_token(mock_token, mock_db)
        
        assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Token has expired" in exc_info.value.detail
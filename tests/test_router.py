import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from src.main import app
from src.auth.schemas import LoginRequest, LoginResponse, RefreshRequest, RefreshResponse
from src.auth.crud import get_user_by_email, create_refresh_token_record, revoke_refresh_token_record
from src.auth.dependencies import get_refresh_token
from src.auth.exceptions import InvalidCredentialsError, TokenRevokedError, TokenExpiredError


client = TestClient(app)


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def mock_user():
    return {
        "id": "user123",
        "email": "test@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
    }


@pytest.fixture
def mock_refresh_token():
    return {
        "id": "token123",
        "user_id": "user123",
        "token": "refresh_token_123",
        "expires_at": datetime.utcnow() + timedelta(days=7),
        "revoked": False
    }


@pytest.fixture
def mock_token_data():
    return {
        "user_id": "user123",
        "email": "test@example.com"
    }


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_user_by_email')
@patch('src.auth.router.verify_password')
@patch('src.auth.router.create_access_token')
@patch('src.auth.router.create_refresh_token')
@patch('src.auth.router.create_refresh_token_record')
def test_login_success(
    mock_create_record,
    mock_create_refresh,
    mock_create_access,
    mock_verify_password,
    mock_get_user,
    mock_get_db,
    mock_user
):
    """Test login endpoint returns tokens on successful authentication."""
    mock_get_db.return_value = MagicMock()
    mock_get_user.return_value = mock_user
    mock_verify_password.return_value = True
    mock_create_access.return_value = "access_token_123"
    mock_create_refresh.return_value = "refresh_token_123"
    mock_create_record.return_value = MagicMock()
    
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "password123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_user_by_email')
@patch('src.auth.router.verify_password')
def test_login_invalid_credentials(mock_verify_password, mock_get_user, mock_get_db):
    """Test login endpoint returns 401 for invalid credentials."""
    mock_get_db.return_value = MagicMock()
    mock_get_user.return_value = {"hashed_password": "some_hash"}
    mock_verify_password.return_value = False
    
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"}
    )
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_user_by_email')
@patch('src.auth.router.verify_password')
def test_login_user_not_found(mock_verify_password, mock_get_user, mock_get_db):
    """Test login endpoint returns 401 when user not found."""
    mock_get_db.return_value = MagicMock()
    mock_get_user.return_value = None
    
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "password123"}
    )
    
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_refresh_token')
@patch('src.auth.router.revoke_refresh_token_record')
def test_logout_success(
    mock_revoke,
    mock_get_refresh_token,
    mock_get_db,
    mock_refresh_token
):
    """Test logout endpoint revokes refresh token successfully."""
    mock_get_db.return_value = MagicMock()
    mock_get_refresh_token.return_value = "user123"
    mock_revoke.return_value = mock_refresh_token
    
    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer refresh_token_123"}
    )
    
    assert response.status_code == 204


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_refresh_token')
@patch('src.auth.router.revoke_refresh_token_record')
def test_logout_invalid_token(
    mock_revoke,
    mock_get_refresh_token,
    mock_get_db
):
    """Test logout endpoint returns 401 for invalid refresh token."""
    mock_get_db.return_value = MagicMock()
    mock_get_refresh_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )
    
    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_refresh_token')
@patch('src.auth.router.create_access_token')
def test_refresh_success(
    mock_create_access,
    mock_get_refresh_token,
    mock_get_db,
    mock_token_data
):
    """Test refresh endpoint returns new access token."""
    mock_get_db.return_value = MagicMock()
    mock_get_refresh_token.return_value = "user123"
    mock_create_access.return_value = "new_access_token_123"
    
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "valid_refresh_token"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_refresh_token')
def test_refresh_invalid_token(mock_get_refresh_token, mock_get_db):
    """Test refresh endpoint returns 401 for invalid refresh token."""
    mock_get_db.return_value = MagicMock()
    mock_get_refresh_token.side_effect = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token"
    )
    
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    
    assert response.status_code == 401
    assert "Invalid refresh token" in response.json()["detail"]


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_refresh_token')
def test_refresh_revoked_token(mock_get_refresh_token, mock_get_db):
    """Test refresh endpoint returns 401 for revoked refresh token."""
    mock_get_db.return_value = MagicMock()
    mock_get_refresh_token.side_effect = TokenRevokedError("Token has been revoked")
    
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "revoked_token"}
    )
    
    assert response.status_code == 401
    assert "Token has been revoked" in response.json()["detail"]


@patch('src.auth.router.get_db')
@patch('src.auth.router.get_refresh_token')
def test_refresh_expired_token(mock_get_refresh_token, mock_get_db):
    """Test refresh endpoint returns 401 for expired refresh token."""
    mock_get_db.return_value = MagicMock()
    mock_get_refresh_token.side_effect = TokenExpiredError("Token has expired")
    
    response = client.post(
        "/auth/refresh",
        json={"refresh_token": "expired_token"}
    )
    
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]
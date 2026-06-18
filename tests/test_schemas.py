import pytest
from pydantic import ValidationError
from src.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RefreshResponse,
    TokenData
)
from datetime import datetime


def test_login_request_valid():
    """Test LoginRequest with valid data."""
    request = LoginRequest(email="test@example.com", password="password123")
    assert request.email == "test@example.com"
    assert request.password == "password123"


def test_login_request_invalid_email():
    """Test LoginRequest with invalid email format."""
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(email="invalid_email", password="password123")
    assert "email" in str(exc_info.value)


def test_login_request_empty_password():
    """Test LoginRequest with empty password."""
    with pytest.raises(ValidationError) as exc_info:
        LoginRequest(email="test@example.com", password="")
    assert "password" in str(exc_info.value)


def test_login_response_valid():
    """Test LoginResponse with valid data."""
    response = LoginResponse(
        access_token="access_token_123",
        refresh_token="refresh_token_123",
        token_type="bearer"
    )
    assert response.access_token == "access_token_123"
    assert response.refresh_token == "refresh_token_123"
    assert response.token_type == "bearer"


def test_login_response_missing_fields():
    """Test LoginResponse fails when required fields are missing."""
    with pytest.raises(ValidationError) as exc_info:
        LoginResponse()
    assert "access_token" in str(exc_info.value) or "refresh_token" in str(exc_info.value)


def test_refresh_request_valid():
    """Test RefreshRequest with valid data."""
    request = RefreshRequest(refresh_token="refresh_token_123")
    assert request.refresh_token == "refresh_token_123"


def test_refresh_request_empty_token():
    """Test RefreshRequest with empty token."""
    with pytest.raises(ValidationError) as exc_info:
        RefreshRequest(refresh_token="")
    assert "refresh_token" in str(exc_info.value)


def test_refresh_response_valid():
    """Test RefreshResponse with valid data."""
    response = RefreshResponse(access_token="new_access_token_123", token_type="bearer")
    assert response.access_token == "new_access_token_123"
    assert response.token_type == "bearer"


def test_refresh_response_missing_access_token():
    """Test RefreshResponse fails when access_token is missing."""
    with pytest.raises(ValidationError) as exc_info:
        RefreshResponse(token_type="bearer")
    assert "access_token" in str(exc_info.value)


def test_token_data_valid():
    """Test TokenData with valid data."""
    token_data = TokenData(
        user_id="user123",
        email="test@example.com",
        scopes=["read", "write"]
    )
    assert token_data.user_id == "user123"
    assert token_data.email == "test@example.com"
    assert token_data.scopes == ["read", "write"]


def test_token_data_optional_fields():
    """Test TokenData with optional fields missing."""
    token_data = TokenData()
    assert token_data.user_id is None
    assert token_data.email is None
    assert token_data.scopes is None


def test_token_data_invalid_email():
    """Test TokenData with invalid email format."""
    with pytest.raises(ValidationError) as exc_info:
        TokenData(email="invalid_email")
    assert "email" in str(exc_info.value)
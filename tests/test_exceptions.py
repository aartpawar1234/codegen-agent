import pytest
from src.auth.exceptions import (
    InvalidCredentialsError,
    TokenRevokedError,
    TokenExpiredError
)


def test_invalid_credentials_error():
    """Test InvalidCredentialsError has correct status code and detail."""
    with pytest.raises(InvalidCredentialsError) as exc_info:
        raise InvalidCredentialsError()
    
    assert exc_info.value.status_code == 401
    assert "Invalid credentials" in exc_info.value.detail
    assert "WWW-Authenticate" in exc_info.value.headers


def test_token_revoked_error():
    """Test TokenRevokedError has correct status code and detail."""
    with pytest.raises(TokenRevokedError) as exc_info:
        raise TokenRevokedError()
    
    assert exc_info.value.status_code == 401
    assert "Token has been revoked" in exc_info.value.detail
    assert "WWW-Authenticate" in exc_info.value.headers


def test_token_expired_error():
    """Test TokenExpiredError has correct status code and detail."""
    with pytest.raises(TokenExpiredError) as exc_info:
        raise TokenExpiredError()
    
    assert exc_info.value.status_code == 401
    assert "Token has expired" in exc_info.value.detail
    assert "WWW-Authenticate" in exc_info.value.headers
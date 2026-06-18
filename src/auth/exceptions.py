from fastapi import HTTPException, status

class InvalidCredentialsError(HTTPException):
    """Exception raised when credentials are invalid."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class TokenRevokedError(HTTPException):
    """Exception raised when refresh token is revoked."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
        )

class TokenExpiredError(HTTPException):
    """Exception raised when token is expired."""
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
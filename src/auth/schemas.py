from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    """Request schema for login endpoint."""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Response schema for login endpoint."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    """Request schema for refresh endpoint."""
    refresh_token: str

class RefreshResponse(BaseModel):
    """Response schema for refresh endpoint."""
    access_token: str
    token_type: str = "bearer"
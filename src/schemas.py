"""
Pydantic schemas for request and response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema containing user email."""

    email: Optional[str] = None


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for user creation request."""

    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserResponse(UserBase):
    """Schema for user response."""

    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

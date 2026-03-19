"""
Pydantic schemas for user authentication flows.
"""
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for signup request body."""
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    """Schema for login request body."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public-safe user object returned to the frontend."""
    id: str
    full_name: str
    email: str


class TokenResponse(BaseModel):
    """Response containing the JWT access token."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

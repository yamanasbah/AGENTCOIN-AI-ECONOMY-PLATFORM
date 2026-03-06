from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.models import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserProfileResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True

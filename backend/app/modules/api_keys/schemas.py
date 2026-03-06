from datetime import datetime

from pydantic import BaseModel, Field


class APIKeyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class APIKeyRead(BaseModel):
    id: int
    name: str
    key: str
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True

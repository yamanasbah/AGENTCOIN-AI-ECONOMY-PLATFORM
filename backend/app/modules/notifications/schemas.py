from datetime import datetime

from pydantic import BaseModel


class NotificationRead(BaseModel):
    id: int
    title: str
    message: str
    read: bool
    created_at: datetime

    class Config:
        from_attributes = True

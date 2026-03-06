from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AgentTaskRead(BaseModel):
    id: int
    agent_id: str
    task_type: str
    payload: dict[str, Any]
    status: str
    created_at: datetime
    finished_at: datetime | None

    class Config:
        from_attributes = True

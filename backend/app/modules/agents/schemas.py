from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.modules.agents.models import AgentStatus, AgentStrategyType


class AgentCreateRequest(BaseModel):
    name: str
    description: str | None = None
    strategy_type: AgentStrategyType


class AgentRead(BaseModel):
    id: UUID
    owner_user_id: int
    name: str
    description: str | None
    strategy_type: AgentStrategyType
    status: AgentStatus
    docker_container_id: str | None
    wallet_id: UUID
    revenue_generated: float
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.agents.models import AgentStatus, AgentStrategyType


class AgentCreateRequest(BaseModel):
    name: str
    description: str | None = None
    strategy_type: AgentStrategyType
    initial_capital: float = Field(gt=0)


class AgentActionRequest(BaseModel):
    agent_id: UUID


class AgentRead(BaseModel):
    id: UUID
    owner_user_id: int
    name: str
    description: str | None
    strategy_type: AgentStrategyType
    initial_capital: float
    wallet_id: UUID
    status: AgentStatus
    created_at: datetime

    class Config:
        from_attributes = True

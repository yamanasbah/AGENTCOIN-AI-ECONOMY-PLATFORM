from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.agents.models import AgentStatus, AgentType


class AgentCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = None
    agent_type: AgentType
    system_prompt: str = Field(min_length=1)
    capabilities: dict = Field(default_factory=dict)
    is_public: bool = False


class AgentUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    system_prompt: str | None = Field(default=None, min_length=1)
    capabilities: dict | None = None
    is_public: bool | None = None
    status: AgentStatus | None = None


class AgentRead(BaseModel):
    id: UUID
    tenant_id: str
    owner_user_id: int
    name: str
    description: str | None
    agent_type: AgentType
    system_prompt: str
    capabilities: dict
    is_public: bool
    status: AgentStatus
    wallet_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class AgentRunRequest(BaseModel):
    input: str = Field(min_length=1)


class AgentRunResponse(BaseModel):
    agent_id: UUID
    result: str
    tokens_used: int
    execution_cost: float


class AgentLeaderboardEntry(BaseModel):
    id: UUID
    name: str
    owner_user_id: int
    total_earnings: float
    total_runs: int

    class Config:
        from_attributes = True


class CreatorStatsResponse(BaseModel):
    total_agents: int
    total_earnings: float
    total_runs: int

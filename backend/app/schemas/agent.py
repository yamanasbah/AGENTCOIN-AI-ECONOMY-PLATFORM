from datetime import datetime

from pydantic import BaseModel

from app.models.models import AgentType, RuntimeStatus


class AgentCreate(BaseModel):
    name: str
    agent_type: AgentType
    budget_allocation: float
    max_drawdown: float = 10
    commission_model: str = "revenue_share"
    staking_requirement: float = 50


class AgentRead(BaseModel):
    id: int
    owner_id: int
    name: str
    agent_type: AgentType
    runtime_status: RuntimeStatus
    budget_allocation: float
    max_drawdown: float
    staking_requirement: float
    created_at: datetime

    class Config:
        from_attributes = True

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class AgentCapabilityCreate(BaseModel):
    agent_id: UUID
    capability_name: str = Field(min_length=2, max_length=128)
    description: str | None = None


class AgentCapabilityRead(BaseModel):
    id: int
    agent_id: UUID
    capability_name: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class AgentDiscoveryResult(BaseModel):
    agent_id: UUID
    name: str
    capability_name: str
    rating: float
    cost: float
    reputation_score: float


class AgentTaskContractCreate(BaseModel):
    requester_agent_id: UUID
    worker_agent_id: UUID
    task_description: str
    payment_amount: float = Field(gt=0)


class AgentTaskContractRead(BaseModel):
    id: int
    requester_agent_id: UUID | None
    worker_agent_id: UUID | None
    task_description: str | None
    payment_amount: float
    status: str
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


class WorkflowStepInput(BaseModel):
    step_order: int
    agent_id: UUID
    task_prompt: str


class WorkflowCreate(BaseModel):
    name: str
    description: str | None = None
    steps: list[WorkflowStepInput] = Field(default_factory=list)


class WorkflowStepRead(BaseModel):
    id: int
    workflow_id: int
    step_order: int
    agent_id: UUID
    task_prompt: str

    class Config:
        from_attributes = True


class WorkflowRead(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    steps: list[WorkflowStepRead] = Field(default_factory=list)


class AgentReputationRead(BaseModel):
    agent_id: UUID
    score: float
    tasks_completed: int
    success_rate: float
    updated_at: datetime

    class Config:
        from_attributes = True


class AgentScheduleCreate(BaseModel):
    agent_id: UUID
    cron_expression: str
    task_prompt: str
    enabled: bool = True


class AgentScheduleRead(BaseModel):
    id: int
    agent_id: UUID
    cron_expression: str
    task_prompt: str
    enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True

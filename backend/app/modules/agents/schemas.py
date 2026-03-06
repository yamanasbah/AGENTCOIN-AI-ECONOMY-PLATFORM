from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.agents.models import AgentStatus, AgentType

AGENT_CATEGORIES = [
    "Marketing",
    "Trading",
    "Research",
    "Content",
    "Automation",
    "Crypto",
    "Productivity",
]


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


class AgentPublishRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    category: str = Field(min_length=1, max_length=64)
    tags: list[str] = Field(default_factory=list)
    price_per_run: float = Field(gt=0)
    price_per_month: float = Field(ge=0)


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
    is_published: bool
    price_per_run: float
    price_per_month: float
    category: str | None
    tags: list[str]
    rating: float
    status: AgentStatus
    wallet_id: UUID
    is_autonomous: bool
    run_interval_seconds: int
    total_earnings: float
    total_runs: int
    total_revenue: float
    last_run_at: datetime | None
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


class AgentAsyncRunResponse(BaseModel):
    task_id: int
    status: str


class StoreAgentRead(BaseModel):
    id: int
    agent_id: UUID
    title: str
    description: str | None
    category: str | None
    price_per_run: float
    price_per_month: float
    rating: float
    usage_count: int
    created_at: datetime
    creator_user_id: int
    creator_username: str
    total_runs: int


class InstallAgentResponse(BaseModel):
    id: int
    user_id: int
    agent_id: UUID
    installed_at: datetime
    active: bool

    class Config:
        from_attributes = True


class AgentReviewRequest(BaseModel):
    agent_id: UUID
    rating: int = Field(ge=1, le=5)
    review: str | None = None


class AgentReviewRead(BaseModel):
    id: int
    agent_id: UUID
    user_id: int
    rating: int
    review: str | None
    created_at: datetime

    class Config:
        from_attributes = True

import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AgentType(str, enum.Enum):
    marketing_agent = "marketing_agent"
    trading_agent = "trading_agent"
    research_agent = "research_agent"
    automation_agent = "automation_agent"
    custom_agent = "custom_agent"


class AgentStatus(str, enum.Enum):
    idle = "idle"
    running = "running"
    paused = "paused"


class ManagedAgent(Base):
    __tablename__ = "managed_agents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    agent_type: Mapped[AgentType] = mapped_column(Enum(AgentType, name="agenttype"), nullable=False)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    capabilities: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=False, nullable=False)
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus, name="agentlifecyclestatus"), default=AgentStatus.idle, nullable=False)
    wallet_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False)
    total_earnings: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    total_runs: Mapped[int] = mapped_column(default=0, nullable=False)
    average_rating: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    success_rate: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    is_autonomous: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    run_interval_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=300)
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    execution_message: Mapped[str] = mapped_column(Text, nullable=False)
    tokens_consumed: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    input_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    output_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    execution_cost: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    tokens_used: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    execution_time: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="success")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AgentTask(Base):
    __tablename__ = "agent_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    task_type: Mapped[str] = mapped_column(String(64), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

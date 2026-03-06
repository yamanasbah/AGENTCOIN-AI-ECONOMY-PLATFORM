from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AgentCapability(Base):
    __tablename__ = "agent_capabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    capability_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AgentWorkflow(Base):
    __tablename__ = "agent_workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("agent_workflows.id", ondelete="CASCADE"), nullable=False, index=True)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)
    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    task_prompt: Mapped[str] = mapped_column(Text, nullable=False)


class AgentReputation(Base):
    __tablename__ = "agent_reputation"

    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), primary_key=True)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    tasks_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    success_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class AgentSchedule(Base):
    __tablename__ = "agent_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    cron_expression: Mapped[str] = mapped_column(String(120), nullable=False)
    task_prompt: Mapped[str] = mapped_column(Text, nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

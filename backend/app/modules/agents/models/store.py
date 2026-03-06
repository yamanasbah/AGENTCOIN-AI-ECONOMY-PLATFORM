import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AgentStoreListing(Base):
    __tablename__ = "agent_store_listings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True, unique=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    category: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    price_per_run: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=1)
    price_per_month: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False, default=0)
    rating: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    usage_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class InstalledAgent(Base):
    __tablename__ = "installed_agents"
    __table_args__ = (UniqueConstraint("user_id", "agent_id", name="uq_installed_agents_user_agent"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    installed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)


class AgentReview(Base):
    __tablename__ = "agent_reviews"
    __table_args__ = (UniqueConstraint("agent_id", "user_id", name="uq_agent_reviews_agent_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("managed_agents.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

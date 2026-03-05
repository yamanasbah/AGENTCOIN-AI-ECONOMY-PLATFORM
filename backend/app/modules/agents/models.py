import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AgentStrategyType(str, enum.Enum):
    trading = "trading"
    marketing = "marketing"
    research = "research"
    arbitrage = "arbitrage"
    social = "social"


class AgentStatus(str, enum.Enum):
    created = "created"
    running = "running"
    stopped = "stopped"


class ManagedAgent(Base):
    __tablename__ = "managed_agents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    strategy_type: Mapped[AgentStrategyType] = mapped_column(Enum(AgentStrategyType, name="agentstrategytype"), nullable=False)
    status: Mapped[AgentStatus] = mapped_column(Enum(AgentStatus, name="agentstatus"), default=AgentStatus.created, nullable=False)
    docker_container_id: Mapped[str | None] = mapped_column(String(128))
    wallet_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False)
    revenue_generated: Mapped[float] = mapped_column(Numeric(18, 4), default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

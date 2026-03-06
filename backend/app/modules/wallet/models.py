import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class WalletOwnerType(str, enum.Enum):
    user = "user"
    agent = "agent"
    treasury = "treasury"


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_type: Mapped[WalletOwnerType] = mapped_column(Enum(WalletOwnerType, name="walletownertype"), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    balance: Mapped[float] = mapped_column(Numeric(18, 4), default=0, nullable=False)
    locked_balance: Mapped[float] = mapped_column(Numeric(18, 4), default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class TransactionType(str, enum.Enum):
    transfer = "transfer"
    stake = "stake"
    unstake = "unstake"
    execution = "execution"
    marketplace_purchase = "marketplace_purchase"


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_wallet_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=True, index=True)
    to_wallet_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    type: Mapped[TransactionType] = mapped_column(Enum(TransactionType, name="transactiontype"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Stake(Base):
    __tablename__ = "stakes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wallets.id"), nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(18, 4), nullable=False)
    reward_rate: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    unlock_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

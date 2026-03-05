from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.wallet.models import TransactionType


class WalletRead(BaseModel):
    id: UUID
    user_id: int
    agc_balance: float
    staked_balance: float
    created_at: datetime

    class Config:
        from_attributes = True


class WalletTransactionRead(BaseModel):
    id: UUID
    wallet_id: UUID
    type: TransactionType
    amount: float
    reason: str
    created_at: datetime

    class Config:
        from_attributes = True


class WalletTransferRequest(BaseModel):
    amount: float = Field(gt=0)
    recipient_user_id: int

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.modules.wallet.models import TokenTransactionType, WalletOwnerType


class WalletRead(BaseModel):
    id: UUID
    owner_type: WalletOwnerType
    owner_id: str
    balance: float
    locked_balance: float
    created_at: datetime

    class Config:
        from_attributes = True


class WalletDepositRequest(BaseModel):
    amount: float = Field(gt=0)


class WalletTransferRequest(BaseModel):
    recipient_wallet_id: UUID
    amount: float = Field(gt=0)


class WalletTransactionRead(BaseModel):
    id: UUID
    wallet_id: UUID
    amount: float
    type: TokenTransactionType
    created_at: datetime

    class Config:
        from_attributes = True

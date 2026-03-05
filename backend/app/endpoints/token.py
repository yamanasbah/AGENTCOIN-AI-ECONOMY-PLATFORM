from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.wallet.models import Stake, WalletOwnerType
from app.modules.wallet.service import WalletService

router = APIRouter()


class StakeRequest(BaseModel):
    amount: float = Field(gt=0)
    reward_rate: float = Field(default=0.08, gt=0)


class UnstakeRequest(BaseModel):
    stake_id: UUID


@router.post("/stake")
def stake_tokens(payload: StakeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    try:
        WalletService.lock_funds(wallet, payload.amount)
        stake = Stake(wallet_id=wallet.id, amount=payload.amount, reward_rate=payload.reward_rate)
        db.add(stake)
        db.commit()
        return {"stake_id": str(stake.id), "amount": payload.amount, "reward_rate": payload.reward_rate}
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/unstake")
def unstake_tokens(payload: UnstakeRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    stake = db.query(Stake).filter(Stake.id == payload.stake_id, Stake.wallet_id == wallet.id).first()
    if not stake:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stake not found")

    WalletService.unlock_funds(wallet, float(stake.amount))
    db.delete(stake)
    db.commit()
    return {"unstaked": True}


@router.get("/balance")
def token_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    return {
        "token": "AGC",
        "balance": float(wallet.balance),
        "locked_balance": float(wallet.locked_balance),
        "available": float(wallet.balance) - float(wallet.locked_balance),
    }

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.wallet.models import Wallet, WalletTransaction
from app.modules.wallet.schemas import WalletRead, WalletTransactionRead, WalletTransferRequest
from app.modules.wallet.service import WalletService

router = APIRouter()


@router.get("", response_model=WalletRead)
def get_wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, current_user.id)
    db.commit()
    db.refresh(wallet)
    return wallet


@router.get("/transactions", response_model=list[WalletTransactionRead])
def get_wallet_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, current_user.id)
    db.commit()
    return (
        db.query(WalletTransaction)
        .filter(WalletTransaction.wallet_id == wallet.id)
        .order_by(WalletTransaction.created_at.desc())
        .all()
    )


@router.post("/transfer", response_model=WalletRead)
def transfer_tokens(payload: WalletTransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    source_wallet = WalletService.get_or_create_wallet(db, current_user.id)
    recipient_wallet = db.query(Wallet).filter(Wallet.user_id == payload.recipient_user_id).first()
    if not recipient_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient wallet not found")

    try:
        WalletService.debit(db, source_wallet, payload.amount, f"transfer_to:{payload.recipient_user_id}")
        WalletService.credit(db, recipient_wallet, payload.amount, f"transfer_from:{current_user.id}")
        db.commit()
        db.refresh(source_wallet)
        return source_wallet
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.wallet.models import Transaction, Wallet, WalletOwnerType
from app.modules.wallet.schemas import WalletDepositRequest, WalletRead, WalletTransactionRead, WalletTransferRequest
from app.modules.wallet.service import WalletService

router = APIRouter()


@router.get("", response_model=WalletRead)
def get_wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    db.commit()
    db.refresh(wallet)
    return wallet


@router.post("/deposit", response_model=WalletRead)
def deposit_wallet(payload: WalletDepositRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    wallet.balance = float(wallet.balance) + payload.amount
    db.commit()
    db.refresh(wallet)
    return wallet


@router.post("/transfer", response_model=WalletRead)
def transfer_wallet(payload: WalletTransferRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    source_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    destination_wallet = db.query(Wallet).filter(Wallet.id == payload.recipient_wallet_id).first()
    if not destination_wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipient wallet not found")
    try:
        WalletService.transfer_tokens(db, source_wallet, destination_wallet, payload.amount)
        db.commit()
        db.refresh(source_wallet)
        return source_wallet
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/transactions", response_model=list[WalletTransactionRead])
def wallet_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    db.commit()
    return (
        db.query(Transaction)
        .filter((Transaction.from_wallet_id == wallet.id) | (Transaction.to_wallet_id == wallet.id))
        .order_by(Transaction.created_at.desc())
        .all()
    )

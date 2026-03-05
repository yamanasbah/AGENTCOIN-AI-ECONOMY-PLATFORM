from sqlalchemy.orm import Session

from app.modules.wallet.models import TransactionType, Wallet, WalletTransaction


class WalletService:
    @staticmethod
    def get_or_create_wallet(db: Session, user_id: int) -> Wallet:
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if wallet:
            return wallet
        wallet = Wallet(user_id=user_id, agc_balance=500)
        db.add(wallet)
        db.flush()
        return wallet

    @staticmethod
    def create_transaction(db: Session, wallet_id, tx_type: TransactionType, amount: float, reason: str) -> WalletTransaction:
        transaction = WalletTransaction(wallet_id=wallet_id, type=tx_type, amount=amount, reason=reason)
        db.add(transaction)
        return transaction

    @staticmethod
    def debit(db: Session, wallet: Wallet, amount: float, reason: str) -> None:
        if float(wallet.agc_balance) < amount:
            raise ValueError("Insufficient AGC balance")
        wallet.agc_balance = float(wallet.agc_balance) - amount
        WalletService.create_transaction(db, wallet.id, TransactionType.debit, amount, reason)

    @staticmethod
    def credit(db: Session, wallet: Wallet, amount: float, reason: str) -> None:
        wallet.agc_balance = float(wallet.agc_balance) + amount
        WalletService.create_transaction(db, wallet.id, TransactionType.credit, amount, reason)

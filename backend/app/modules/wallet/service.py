from sqlalchemy.orm import Session

from app.modules.wallet.models import Transaction, TransactionType, Wallet, WalletOwnerType


class WalletService:
    @staticmethod
    def create_wallet(db: Session, owner_type: WalletOwnerType, owner_id: str, initial_balance: float = 0.0) -> Wallet:
        wallet = Wallet(owner_type=owner_type, owner_id=str(owner_id), balance=initial_balance, locked_balance=0)
        db.add(wallet)
        db.flush()
        return wallet

    @staticmethod
    def get_wallet(db: Session, owner_type: WalletOwnerType, owner_id: str) -> Wallet | None:
        return db.query(Wallet).filter(Wallet.owner_type == owner_type, Wallet.owner_id == str(owner_id)).first()

    @staticmethod
    def get_wallet_by_id(db: Session, wallet_id) -> Wallet:
        wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
        if not wallet:
            raise ValueError("Wallet not found")
        return wallet

    @staticmethod
    def get_or_create_wallet(db: Session, owner_type: WalletOwnerType, owner_id: str, initial_balance: float = 0.0) -> Wallet:
        wallet = WalletService.get_wallet(db, owner_type, owner_id)
        if wallet:
            return wallet
        return WalletService.create_wallet(db, owner_type, owner_id, initial_balance=initial_balance)

    @staticmethod
    def transfer_tokens(db: Session, from_wallet: Wallet, to_wallet: Wallet, amount: float, tx_type: TransactionType = TransactionType.transfer) -> None:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        available = float(from_wallet.balance) - float(from_wallet.locked_balance)
        if available < amount:
            raise ValueError("Insufficient available balance")

        from_wallet.balance = float(from_wallet.balance) - amount
        to_wallet.balance = float(to_wallet.balance) + amount
        db.add(Transaction(from_wallet_id=from_wallet.id, to_wallet_id=to_wallet.id, amount=amount, type=tx_type))

    @staticmethod
    def lock_tokens(db: Session, wallet: Wallet, amount: float) -> Wallet:
        if amount <= 0:
            raise ValueError("Lock amount must be positive")
        available = float(wallet.balance) - float(wallet.locked_balance)
        if available < amount:
            raise ValueError("Insufficient available balance")
        wallet.locked_balance = float(wallet.locked_balance) + amount
        db.add(Transaction(from_wallet_id=wallet.id, to_wallet_id=None, amount=amount, type=TransactionType.stake))
        return wallet

    @staticmethod
    def unlock_tokens(db: Session, wallet: Wallet, amount: float) -> Wallet:
        if amount <= 0:
            raise ValueError("Unlock amount must be positive")
        if float(wallet.locked_balance) < amount:
            raise ValueError("Insufficient locked balance")
        wallet.locked_balance = float(wallet.locked_balance) - amount
        db.add(Transaction(from_wallet_id=None, to_wallet_id=wallet.id, amount=amount, type=TransactionType.unstake))
        return wallet

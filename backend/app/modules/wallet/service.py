from sqlalchemy.orm import Session

from app.modules.wallet.models import TokenTransaction, TokenTransactionType, Wallet, WalletOwnerType


class WalletService:
    @staticmethod
    def create_wallet(db: Session, owner_type: WalletOwnerType, owner_id: str, initial_balance: float = 0.0) -> Wallet:
        wallet = Wallet(owner_type=owner_type, owner_id=str(owner_id), balance=initial_balance, locked_balance=0)
        db.add(wallet)
        db.flush()
        if initial_balance > 0:
            WalletService._record_tx(db, wallet.id, initial_balance, TokenTransactionType.mint)
        return wallet

    @staticmethod
    def get_wallet(db: Session, owner_type: WalletOwnerType, owner_id: str) -> Wallet | None:
        return (
            db.query(Wallet)
            .filter(Wallet.owner_type == owner_type, Wallet.owner_id == str(owner_id))
            .first()
        )

    @staticmethod
    def get_or_create_wallet(db: Session, owner_type: WalletOwnerType, owner_id: str, initial_balance: float = 0.0) -> Wallet:
        wallet = WalletService.get_wallet(db, owner_type, owner_id)
        if wallet:
            return wallet
        return WalletService.create_wallet(db, owner_type, owner_id, initial_balance=initial_balance)

    @staticmethod
    def deposit(db: Session, wallet: Wallet, amount: float, tx_type: TokenTransactionType = TokenTransactionType.mint) -> Wallet:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        wallet.balance = float(wallet.balance) + amount
        WalletService._record_tx(db, wallet.id, amount, tx_type)
        return wallet

    @staticmethod
    def withdraw(db: Session, wallet: Wallet, amount: float, tx_type: TokenTransactionType = TokenTransactionType.transfer) -> Wallet:
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        available = float(wallet.balance) - float(wallet.locked_balance)
        if available < amount:
            raise ValueError("Insufficient available balance")
        wallet.balance = float(wallet.balance) - amount
        WalletService._record_tx(db, wallet.id, -amount, tx_type)
        return wallet

    @staticmethod
    def transfer(db: Session, source_wallet: Wallet, destination_wallet: Wallet, amount: float) -> None:
        WalletService.withdraw(db, source_wallet, amount, tx_type=TokenTransactionType.transfer)
        WalletService.deposit(db, destination_wallet, amount, tx_type=TokenTransactionType.transfer)

    @staticmethod
    def lock_funds(wallet: Wallet, amount: float) -> Wallet:
        if amount <= 0:
            raise ValueError("Lock amount must be positive")
        available = float(wallet.balance) - float(wallet.locked_balance)
        if available < amount:
            raise ValueError("Insufficient available balance")
        wallet.locked_balance = float(wallet.locked_balance) + amount
        return wallet

    @staticmethod
    def unlock_funds(wallet: Wallet, amount: float) -> Wallet:
        if amount <= 0:
            raise ValueError("Unlock amount must be positive")
        if float(wallet.locked_balance) < amount:
            raise ValueError("Insufficient locked balance")
        wallet.locked_balance = float(wallet.locked_balance) - amount
        return wallet

    @staticmethod
    def _record_tx(db: Session, wallet_id, amount: float, tx_type: TokenTransactionType) -> None:
        db.add(TokenTransaction(wallet_id=wallet_id, amount=amount, type=tx_type))

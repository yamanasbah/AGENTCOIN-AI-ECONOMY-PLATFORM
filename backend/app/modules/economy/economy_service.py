from sqlalchemy.orm import Session

from app.modules.agents.models import ManagedAgent
from app.modules.wallet.models import TokenTransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class EconomyService:
    USER_SHARE = 0.80
    PLATFORM_FEE = 0.10
    BURN = 0.05
    TREASURY = 0.05

    @staticmethod
    def profit_split(amount: float) -> dict[str, float]:
        return {
            "user_share": amount * EconomyService.USER_SHARE,
            "platform_fee": amount * EconomyService.PLATFORM_FEE,
            "burn": amount * EconomyService.BURN,
            "treasury": amount * EconomyService.TREASURY,
        }

    @staticmethod
    def distribute_profit(db: Session, agent: ManagedAgent, amount: float) -> dict[str, float]:
        if amount <= 0:
            return EconomyService.profit_split(0)
        split = EconomyService.profit_split(amount)
        user_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(agent.owner_user_id))
        platform_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, "platform")
        treasury_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, "treasury")

        WalletService.deposit(db, user_wallet, split["user_share"], tx_type=TokenTransactionType.reward)
        WalletService.deposit(db, platform_wallet, split["platform_fee"], tx_type=TokenTransactionType.fee)
        WalletService.deposit(db, treasury_wallet, split["treasury"], tx_type=TokenTransactionType.fee)
        WalletService._record_tx(db, user_wallet.id, -split["burn"], TokenTransactionType.burn)
        return split

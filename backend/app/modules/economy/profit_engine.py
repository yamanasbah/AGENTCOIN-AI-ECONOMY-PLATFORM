from __future__ import annotations

from decimal import Decimal
from typing import Any

from sqlalchemy.orm import Session

from app.modules.agents.models import ManagedAgent
from app.modules.notifications.service import NotificationService
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class ProfitEngine:
    OWNER_SHARE = Decimal("0.70")
    PLATFORM_SHARE = Decimal("0.20")
    TREASURY_SHARE = Decimal("0.10")

    @staticmethod
    def split_revenue(amount: float | Decimal) -> dict[str, Decimal]:
        amount_decimal = Decimal(str(amount))
        creator_amount = (amount_decimal * ProfitEngine.OWNER_SHARE).quantize(Decimal("0.0001"))
        treasury_amount = (amount_decimal * ProfitEngine.PLATFORM_SHARE).quantize(Decimal("0.0001"))
        infrastructure_amount = amount_decimal - creator_amount - treasury_amount

        return {
            "creator": creator_amount,
            "treasury": treasury_amount,
            "infrastructure": infrastructure_amount,
        }

    @staticmethod
    def ensure_platform_wallet(db: Session):
        return WalletService.get_or_create_wallet(db, WalletOwnerType.user, "agent_infra")

    @staticmethod
    def ensure_treasury_wallet(db: Session):
        return WalletService.get_or_create_wallet(db, WalletOwnerType.treasury, "platform_treasury")

    @staticmethod
    def distribute_run_profit(
        db: Session,
        *,
        payer_user_id: int,
        agent: ManagedAgent,
        amount: float | Decimal,
    ) -> dict[str, Any]:
        amount_decimal = Decimal(str(amount))
        if amount_decimal <= 0:
            raise ValueError("amount must be positive")

        payer_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(payer_user_id))
        owner_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(agent.owner_user_id))
        platform_wallet = ProfitEngine.ensure_platform_wallet(db)
        treasury_wallet = ProfitEngine.ensure_treasury_wallet(db)

        split = ProfitEngine.split_revenue(amount_decimal)

        WalletService.transfer_tokens(
            db,
            from_wallet=payer_wallet,
            to_wallet=owner_wallet,
            amount=float(split["creator"]),
            tx_type=TransactionType.execution,
        )
        WalletService.transfer_tokens(
            db,
            from_wallet=payer_wallet,
            to_wallet=treasury_wallet,
            amount=float(split["treasury"]),
            tx_type=TransactionType.execution,
        )
        WalletService.transfer_tokens(
            db,
            from_wallet=payer_wallet,
            to_wallet=platform_wallet,
            amount=float(split["infrastructure"]),
            tx_type=TransactionType.execution,
        )

        NotificationService.create_notification(
            db,
            agent.owner_user_id,
            "Agent generated revenue",
            f"Agent '{agent.name}' generated {amount_decimal} AGC in revenue.",
        )

        return {
            "amount": float(amount_decimal),
            "creator": float(split["creator"]),
            "treasury": float(split["treasury"]),
            "infrastructure": float(split["infrastructure"]),
            "creator_wallet_id": str(owner_wallet.id),
            "infrastructure_wallet_id": str(platform_wallet.id),
            "treasury_wallet_id": str(treasury_wallet.id),
        }

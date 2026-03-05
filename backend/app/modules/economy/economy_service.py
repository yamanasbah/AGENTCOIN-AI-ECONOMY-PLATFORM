from sqlalchemy.orm import Session

from app.modules.agents.models import ManagedAgent
from app.modules.wallet.service import WalletService


AGENT_CREATION_COST = 100.0
AGENT_RUNTIME_COST_PER_DAY = 10.0
MARKETPLACE_COMMISSION_RATE = 0.05


class EconomyService:
    @staticmethod
    def charge_for_agent_creation(db: Session, user_id: int):
        wallet = WalletService.get_or_create_wallet(db, user_id)
        WalletService.debit(db, wallet, AGENT_CREATION_COST, "agent_creation")
        return wallet

    @staticmethod
    def charge_for_agent_runtime(db: Session, agent: ManagedAgent):
        wallet = WalletService.get_or_create_wallet(db, agent.owner_user_id)
        WalletService.debit(db, wallet, AGENT_RUNTIME_COST_PER_DAY, f"agent_runtime:{agent.id}")
        return wallet

    @staticmethod
    def distribute_revenue(db: Session, agent: ManagedAgent, amount: float):
        commission = amount * MARKETPLACE_COMMISSION_RATE
        payout = amount - commission

        owner_wallet = WalletService.get_or_create_wallet(db, agent.owner_user_id)
        WalletService.credit(db, owner_wallet, payout, f"agent_revenue:{agent.id}")

        agent.revenue_generated = float(agent.revenue_generated) + amount
        return {"gross": amount, "commission": commission, "payout": payout}

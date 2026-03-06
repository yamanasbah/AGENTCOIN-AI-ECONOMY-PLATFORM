from sqlalchemy.orm import Session

from app.modules.agents.models import ManagedAgent
from app.modules.economy.profit_engine import ProfitEngine


class EconomyService:
    @staticmethod
    def distribute_profit(db: Session, agent: ManagedAgent, amount: float, payer_user_id: int) -> dict[str, float]:
        return ProfitEngine.distribute_run_profit(
            db,
            payer_user_id=payer_user_id,
            agent=agent,
            amount=amount,
        )

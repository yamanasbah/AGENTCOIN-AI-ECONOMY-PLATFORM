from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import Subscription, User
from app.modules.agents.models import AgentLog, ManagedAgent
from app.modules.wallet.models import Transaction


class AnalyticsService:
    @staticmethod
    def platform_stats(db: Session) -> dict:
        platform_revenue = db.query(func.coalesce(func.sum(Subscription.amount_token), 0)).scalar() or 0
        return {
            "total_users": db.query(func.count(User.id)).scalar() or 0,
            "total_agents": db.query(func.count(ManagedAgent.id)).scalar() or 0,
            "total_runs": db.query(func.count(AgentLog.id)).scalar() or 0,
            "total_transactions": db.query(func.count(Transaction.id)).scalar() or 0,
            "platform_revenue": float(platform_revenue),
        }

from uuid import UUID

from app.db.session import SessionLocal
from app.modules.agents.models import ManagedAgent
from app.modules.agents.strategies import get_strategy
from app.modules.economy.economy_service import EconomyService
from app.workers.celery_app import celery_app


@celery_app.task
def run_agent_strategy(agent_id: str) -> str:
    db = SessionLocal()
    try:
        agent = db.query(ManagedAgent).filter(ManagedAgent.id == UUID(agent_id)).first()
        if not agent:
            return "agent_not_found"
        strategy = get_strategy(agent)
        profit = strategy.execute()
        EconomyService.distribute_profit(db, agent, profit)
        db.commit()
        return f"agent_execution_complete:{profit}"
    finally:
        db.close()

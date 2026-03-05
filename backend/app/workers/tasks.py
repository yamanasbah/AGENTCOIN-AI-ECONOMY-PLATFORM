from uuid import UUID

from app.db.session import SessionLocal
from app.modules.agents.models import ManagedAgent
from app.modules.economy.economy_service import EconomyService
from app.services.onchain_sync_service import sync_placeholder
from app.workers.celery_app import celery_app


@celery_app.task
def run_onchain_sync() -> str:
    sync_placeholder()
    return "sync_complete"


@celery_app.task
def run_agent_strategy(agent_id: str) -> str:
    db = SessionLocal()
    try:
        agent = db.query(ManagedAgent).filter(ManagedAgent.id == UUID(agent_id)).first()
        if not agent:
            return "agent_not_found"
        EconomyService.distribute_revenue(db, agent, amount=25.0)
        db.commit()
        return "agent_execution_complete"
    finally:
        db.close()

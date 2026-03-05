from uuid import UUID

from app.db.session import SessionLocal
from app.modules.agents.models import ManagedAgent
from app.modules.agents.runner import AgentRunner
from app.workers.celery_app import celery_app


@celery_app.task
def run_agent(agent_id: str) -> str:
    db = SessionLocal()
    try:
        agent = db.query(ManagedAgent).filter(ManagedAgent.id == UUID(agent_id)).first()
        if not agent:
            return "agent_not_found"
        AgentRunner.execute(db, agent)
        db.commit()
        return "agent_execution_complete"
    finally:
        db.close()


@celery_app.task
def run_agent_strategy(agent_id: str) -> str:
    return run_agent(agent_id)

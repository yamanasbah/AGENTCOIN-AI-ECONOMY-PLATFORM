from uuid import UUID

from app.db.session import SessionLocal
from app.modules.agents.models import ManagedAgent
from app.modules.agents.runner import AgentRunner
from app.workers.celery_app import celery_app


@celery_app.task
def run_agent(agent_id: str, user_input: str = "") -> dict:
    db = SessionLocal()
    try:
        agent = db.query(ManagedAgent).filter(ManagedAgent.id == UUID(agent_id)).first()
        if not agent:
            return {"status": "agent_not_found"}

        log = AgentRunner.execute(db, agent, user_input=user_input)
        db.commit()
        return {
            "status": "agent_execution_complete",
            "result": log.output_payload,
            "tokens_used": float(log.tokens_used),
            "cost": float(log.tokens_consumed),
        }
    finally:
        db.close()


@celery_app.task
def run_agent_strategy(agent_id: str) -> dict:
    return run_agent(agent_id)

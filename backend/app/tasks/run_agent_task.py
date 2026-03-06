from __future__ import annotations

from uuid import UUID

from app.db.session import SessionLocal
from app.modules.agent_runtime import AgentRuntimeService
from datetime import datetime

from app.modules.agents.models import ManagedAgent
from app.modules.wallet.models import WalletOwnerType
from app.modules.wallet.service import WalletService
from app.workers.celery_app import celery_app


@celery_app.task(name="app.tasks.run_agent_task.run_agent")
def run_agent(agent_id: str, input: str = "") -> dict:
    db = SessionLocal()
    try:
        agent = db.query(ManagedAgent).filter(ManagedAgent.id == UUID(agent_id)).first()
        if not agent:
            return {"status": "agent_not_found"}

        user_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(agent.owner_user_id))
        available = float(user_wallet.balance) - float(user_wallet.locked_balance)
        execution_cost = AgentRuntimeService(db).runner.EXECUTION_COST
        if available < float(execution_cost):
            return {"status": "insufficient_balance", "required": float(execution_cost), "available": available}


        runtime = AgentRuntimeService(db)
        log = runtime.run_agent(agent.id, input, caller_user_id=agent.owner_user_id, charge_tokens=True)
        agent.total_runs = int(agent.total_runs or 0) + 1
        agent.last_run_at = datetime.utcnow()
        db.commit()

        return {
            "status": "completed",
            "agent_id": str(agent.id),
            "result": log.output_text or log.output_payload,
            "tokens_used": float(log.tokens_used),
            "execution_cost": float(log.execution_cost),
        }
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        return {"status": "failed", "error": str(exc)}
    finally:
        db.close()

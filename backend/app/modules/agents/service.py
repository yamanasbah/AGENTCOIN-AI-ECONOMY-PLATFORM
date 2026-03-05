import uuid

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentStatus, ManagedAgent
from app.modules.economy.economy_service import EconomyService
from app.modules.wallet.service import WalletService
from app.workers.tasks import run_agent_strategy


class AgentService:
    @staticmethod
    def create_agent(db: Session, user_id: int, name: str, description: str | None, strategy_type):
        wallet = EconomyService.charge_for_agent_creation(db, user_id)
        agent = ManagedAgent(
            owner_user_id=user_id,
            name=name,
            description=description,
            strategy_type=strategy_type,
            status=AgentStatus.created,
            wallet_id=wallet.id,
        )
        db.add(agent)
        db.flush()
        return agent

    @staticmethod
    def start_agent(db: Session, agent: ManagedAgent):
        EconomyService.charge_for_agent_runtime(db, agent)
        agent.status = AgentStatus.running
        agent.docker_container_id = agent.docker_container_id or f"sim-{uuid.uuid4().hex[:12]}"
        run_agent_strategy.delay(str(agent.id))
        return agent

    @staticmethod
    def stop_agent(agent: ManagedAgent):
        agent.status = AgentStatus.stopped
        return agent

    @staticmethod
    def delete_agent(db: Session, agent: ManagedAgent):
        db.delete(agent)

    @staticmethod
    def list_agents(db: Session, user_id: int):
        return db.query(ManagedAgent).filter(ManagedAgent.owner_user_id == user_id).order_by(ManagedAgent.created_at.desc()).all()

    @staticmethod
    def ensure_wallet(db: Session, user_id: int):
        return WalletService.get_or_create_wallet(db, user_id)

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agent_runtime import AgentRuntimeService
from app.modules.agents.models import AgentStatus, ManagedAgent
from app.modules.wallet.models import WalletOwnerType
from app.modules.wallet.service import WalletService
from app.workers.tasks import run_agent_task


class AgentService:
    @staticmethod
    def create_agent(
        db: Session,
        tenant_id: str,
        user_id: int,
        name: str,
        description: str | None,
        agent_type,
        system_prompt: str,
        capabilities: dict,
        is_public: bool,
    ) -> ManagedAgent:
        agent_wallet = WalletService.create_wallet(db, WalletOwnerType.agent, "pending", initial_balance=0)
        agent = ManagedAgent(
            tenant_id=tenant_id,
            owner_user_id=user_id,
            name=name,
            description=description,
            agent_type=agent_type,
            system_prompt=system_prompt,
            capabilities=capabilities,
            is_public=is_public,
            status=AgentStatus.idle,
            wallet_id=agent_wallet.id,
        )
        db.add(agent)
        db.flush()
        agent_wallet.owner_id = str(agent.id)
        return agent

    @staticmethod
    def list_agents(db: Session, tenant_id: str, user_id: int):
        return (
            db.query(ManagedAgent)
            .filter(ManagedAgent.tenant_id == tenant_id, ManagedAgent.owner_user_id == user_id)
            .order_by(ManagedAgent.created_at.desc())
            .all()
        )

    @staticmethod
    def get_agent(db: Session, tenant_id: str, user_id: int, agent_id: UUID) -> ManagedAgent | None:
        return (
            db.query(ManagedAgent)
            .filter(ManagedAgent.id == agent_id, ManagedAgent.tenant_id == tenant_id, ManagedAgent.owner_user_id == user_id)
            .first()
        )

    @staticmethod
    def update_agent(agent: ManagedAgent, updates: dict) -> ManagedAgent:
        for field, value in updates.items():
            setattr(agent, field, value)
        return agent

    @staticmethod
    def delete_agent(db: Session, agent: ManagedAgent) -> None:
        db.delete(agent)

    @staticmethod
    def trigger_execution(agent_id: UUID, user_input: str = "") -> None:
        run_agent_task.delay(str(agent_id), user_input)

    @staticmethod
    def run_agent(db: Session, agent: ManagedAgent, user_input: str, caller_user_id: int | None = None):
        runtime_service = AgentRuntimeService(db)
        return runtime_service.run_agent(agent.id, user_input, caller_user_id=caller_user_id)

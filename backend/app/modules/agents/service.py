from sqlalchemy.orm import Session

from app.modules.agents.models import AgentStatus, ManagedAgent
from app.modules.wallet.models import WalletOwnerType
from app.modules.wallet.service import WalletService
from app.workers.tasks import run_agent_strategy


class AgentService:
    @staticmethod
    def create_agent(db: Session, user_id: int, name: str, description: str | None, strategy_type, initial_capital: float):
        user_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(user_id))
        WalletService.withdraw(db, user_wallet, initial_capital)

        agent_wallet = WalletService.create_wallet(db, WalletOwnerType.agent, "pending", initial_balance=initial_capital)
        agent = ManagedAgent(
            owner_user_id=user_id,
            name=name,
            description=description,
            strategy_type=strategy_type,
            initial_capital=initial_capital,
            status=AgentStatus.created,
            wallet_id=agent_wallet.id,
        )
        db.add(agent)
        db.flush()
        agent_wallet.owner_id = str(agent.id)
        return agent

    @staticmethod
    def start_agent(agent: ManagedAgent):
        agent.status = AgentStatus.running
        run_agent_strategy.delay(str(agent.id))
        return agent

    @staticmethod
    def pause_agent(agent: ManagedAgent):
        agent.status = AgentStatus.paused
        return agent

    @staticmethod
    def list_agents(db: Session, user_id: int):
        return db.query(ManagedAgent).filter(ManagedAgent.owner_user_id == user_id).order_by(ManagedAgent.created_at.desc()).all()

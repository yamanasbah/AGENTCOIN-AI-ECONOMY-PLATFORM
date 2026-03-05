from sqlalchemy.orm import Session

from app.modules.agents.models import AgentLog, AgentStatus, ManagedAgent
from app.modules.wallet.models import WalletOwnerType
from app.modules.wallet.service import WalletService


class AgentRunner:
    EXECUTION_COST = 1.0

    @staticmethod
    def execute(db: Session, agent: ManagedAgent, caller_user_id: int | None = None) -> AgentLog:
        payer_id = caller_user_id if caller_user_id is not None else agent.owner_user_id
        payer_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(payer_id))
        WalletService.transfer_tokens(db, payer_wallet, WalletService.get_wallet_by_id(db, agent.wallet_id), AgentRunner.EXECUTION_COST)

        agent.status = AgentStatus.running
        message = f"Agent {agent.name} executed with prompt simulation"
        log = AgentLog(agent_id=agent.id, execution_message=message, tokens_consumed=AgentRunner.EXECUTION_COST)
        db.add(log)
        agent.status = AgentStatus.idle
        return log

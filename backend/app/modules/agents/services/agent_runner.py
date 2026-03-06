from decimal import Decimal

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentLog, AgentStatus, ManagedAgent
from app.modules.agents.runtime import AgentRuntime
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class AgentRunner:
    EXECUTION_COST = 1.0

    @staticmethod
    def execute(db: Session, agent: ManagedAgent, user_input: str = "", caller_user_id: int | None = None) -> AgentLog:
        payer_id = caller_user_id if caller_user_id is not None else agent.owner_user_id
        payer_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(payer_id))
        WalletService.transfer_tokens(
            db,
            payer_wallet,
            WalletService.get_wallet_by_id(db, agent.wallet_id),
            AgentRunner.EXECUTION_COST,
            tx_type=TransactionType.execution,
        )

        agent.status = AgentStatus.running
        runtime_result = AgentRuntime.execute(agent, user_input)

        log = AgentLog(
            agent_id=agent.id,
            execution_message=runtime_result.get("output") or "",
            tokens_consumed=Decimal(str(AgentRunner.EXECUTION_COST)),
            input_payload=runtime_result.get("input") or user_input,
            output_payload=runtime_result.get("output") or "",
            tokens_used=Decimal(str(runtime_result.get("tokens_used", 0))),
            execution_time=Decimal(str(runtime_result.get("execution_time", 0))),
            status=runtime_result.get("status", "success"),
        )
        db.add(log)
        agent.status = AgentStatus.idle
        return log

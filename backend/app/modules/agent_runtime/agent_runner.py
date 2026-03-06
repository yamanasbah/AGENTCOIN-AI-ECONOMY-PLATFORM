from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentLog
from app.modules.agent_runtime.execution_engine import ExecutionEngine
from app.modules.agent_runtime.memory_store import AgentMemoryStore
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class AgentRunner:
    EXECUTION_COST = Decimal("1.0")

    def __init__(self, db: Session) -> None:
        self.db = db
        self.memory_store = AgentMemoryStore(db)
        self.engine = ExecutionEngine(db, self.memory_store)

    def run(self, agent_id: UUID, user_input: str, caller_user_id: int | None = None, charge_tokens: bool = True) -> AgentLog:
        agent = self.engine.load_agent(agent_id)

        if charge_tokens:
            payer_id = caller_user_id if caller_user_id is not None else agent.owner_user_id
            self.charge_agc_tokens(agent.wallet_id, payer_id)

        execution = self.engine.run(agent, user_input)
        log: AgentLog = execution["log"]
        log.execution_cost = self.EXECUTION_COST
        log.tokens_consumed = self.EXECUTION_COST
        return log

    def save_memory(self, agent_id: UUID, memory_key: str, memory_value: str):
        return self.memory_store.save_memory(agent_id, memory_key, memory_value)

    def load_memory(self, agent_id: UUID, limit: int = 20):
        return self.memory_store.load_memory(agent_id, limit)

    def charge_agc_tokens(self, agent_wallet_id: UUID, payer_user_id: int) -> None:
        payer_wallet = WalletService.get_or_create_wallet(self.db, WalletOwnerType.user, str(payer_user_id))
        agent_wallet = WalletService.get_wallet_by_id(self.db, agent_wallet_id)
        WalletService.transfer_tokens(
            self.db,
            from_wallet=payer_wallet,
            to_wallet=agent_wallet,
            amount=float(self.EXECUTION_COST),
            tx_type=TransactionType.execution,
        )

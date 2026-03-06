from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentLog, ManagedAgent
from app.modules.agent_runtime.execution_engine import ExecutionEngine
from app.modules.agent_runtime.memory_store import AgentMemoryStore
from app.modules.economy.profit_engine import ProfitEngine


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
            self.charge_and_distribute(agent, payer_id)

        execution = self.engine.run(agent, user_input)
        log: AgentLog = execution["log"]
        log.execution_cost = self.EXECUTION_COST
        log.tokens_consumed = self.EXECUTION_COST

        self.update_agent_economy_metrics(agent, float(self.EXECUTION_COST), succeeded=log.status == "success")
        return log

    def save_memory(self, agent_id: UUID, memory_key: str, memory_value: str):
        return self.memory_store.save_memory(agent_id, memory_key, memory_value)

    def load_memory(self, agent_id: UUID, limit: int = 20):
        return self.memory_store.load_memory(agent_id, limit)

    def charge_and_distribute(self, agent: ManagedAgent, payer_user_id: int) -> None:
        ProfitEngine.distribute_run_profit(
            self.db,
            payer_user_id=payer_user_id,
            agent=agent,
            amount=self.EXECUTION_COST,
        )

    def update_agent_economy_metrics(self, agent: ManagedAgent, amount: float, *, succeeded: bool) -> None:
        previous_runs = int(agent.total_runs or 0)
        next_runs = previous_runs + 1

        agent.total_runs = next_runs
        agent.total_earnings = float(agent.total_earnings or 0) + amount
        successful_runs = ((float(agent.success_rate or 0) * previous_runs) + (1.0 if succeeded else 0.0))
        agent.success_rate = (successful_runs / next_runs) * 100
        agent.last_run_at = datetime.utcnow()

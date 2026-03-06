from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentLog
from app.modules.agent_runtime.agent_runner import AgentRunner


class AgentRuntimeService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.runner = AgentRunner(db)

    def run_agent(self, agent_id: UUID, input_text: str, caller_user_id: int | None = None, charge_tokens: bool = True) -> AgentLog:
        return self.runner.run(agent_id, input_text, caller_user_id=caller_user_id, charge_tokens=charge_tokens)

    def get_agent_logs(self, agent_id: UUID, limit: int = 50) -> list[AgentLog]:
        return (
            self.db.query(AgentLog)
            .filter(AgentLog.agent_id == agent_id)
            .order_by(AgentLog.created_at.desc())
            .limit(limit)
            .all()
        )

from sqlalchemy.orm import Session

from app.modules.agent_runtime import AgentRuntimeService
from app.modules.agents.models import AgentLog, ManagedAgent


class AgentRunner:
    EXECUTION_COST = 1.0

    @staticmethod
    def execute(db: Session, agent: ManagedAgent, user_input: str = "", caller_user_id: int | None = None) -> AgentLog:
        runtime_service = AgentRuntimeService(db)
        return runtime_service.run_agent(agent.id, user_input, caller_user_id=caller_user_id)

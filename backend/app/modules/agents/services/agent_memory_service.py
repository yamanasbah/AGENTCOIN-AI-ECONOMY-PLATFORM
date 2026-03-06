from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentMemory


class AgentMemoryService:
    @staticmethod
    def add_memory(db: Session, agent_id: UUID, role: str, content: str) -> AgentMemory:
        memory = AgentMemory(agent_id=agent_id, role=role, content=content)
        db.add(memory)
        return memory

    @staticmethod
    def get_recent_memory(db: Session, agent_id: UUID, limit: int = 10) -> list[AgentMemory]:
        return (
            db.query(AgentMemory)
            .filter(AgentMemory.agent_id == agent_id)
            .order_by(AgentMemory.created_at.desc())
            .limit(limit)
            .all()[::-1]
        )

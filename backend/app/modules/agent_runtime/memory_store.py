from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.agents.models import AgentMemory


class AgentMemoryStore:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_memory(self, agent_id: UUID, memory_key: str, memory_value: str) -> AgentMemory:
        memory = AgentMemory(agent_id=agent_id, memory_key=memory_key, memory_value=memory_value)
        self.db.add(memory)
        return memory

    def load_memory(self, agent_id: UUID, limit: int = 20) -> list[AgentMemory]:
        return (
            self.db.query(AgentMemory)
            .filter(AgentMemory.agent_id == agent_id)
            .order_by(AgentMemory.created_at.desc())
            .limit(limit)
            .all()[::-1]
        )

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.modules.agent_runtime import AgentRuntimeService
from app.tasks.run_agent_task import run_agent

router = APIRouter()


class RunAgentRequest(BaseModel):
    agent_id: UUID
    input: str = Field(min_length=1)


class RunAgentResponse(BaseModel):
    task_id: str
    status: str


class AgentLogRead(BaseModel):
    id: UUID
    agent_id: UUID
    input_text: str | None
    output_text: str | None
    status: str
    execution_cost: float
    tokens_used: float
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/run-agent", response_model=RunAgentResponse)
def run_agent_endpoint(payload: RunAgentRequest):
    task = run_agent.delay(str(payload.agent_id), payload.input)
    return RunAgentResponse(task_id=task.id, status="queued")


@router.get("/logs/{agent_id}", response_model=list[AgentLogRead])
def get_runtime_logs(agent_id: UUID, db: Session = Depends(get_db)):
    runtime = AgentRuntimeService(db)
    return runtime.get_agent_logs(agent_id)

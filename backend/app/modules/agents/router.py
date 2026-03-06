from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.agents.schemas import (
    AgentAsyncRunResponse,
    AgentCreateRequest,
    AgentLeaderboardEntry,
    AgentPublishRequest,
    AgentRead,
    AgentRunRequest,
    AgentRunResponse,
    AgentUpdateRequest,
    CreatorStatsResponse,
)
from app.modules.agents.service import AgentService

from app.modules.agents.store_service import AgentStoreService

router = APIRouter()


def _get_owned_agent(db: Session, current_user: User, agent_id: UUID):
    agent = AgentService.get_agent(db, current_user.tenant_id, current_user.id, agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent


@router.post("/create", response_model=AgentRead)
def create_agent(payload: AgentCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = AgentService.create_agent(
        db=db,
        tenant_id=current_user.tenant_id,
        user_id=current_user.id,
        name=payload.name,
        description=payload.description,
        agent_type=payload.agent_type,
        system_prompt=payload.system_prompt,
        capabilities=payload.capabilities,
        is_public=payload.is_public,
    )
    db.commit()
    db.refresh(agent)
    return agent


@router.get("", response_model=list[AgentRead])
def list_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AgentService.list_agents(db, current_user.tenant_id, current_user.id)


@router.get("/leaderboard", response_model=list[AgentLeaderboardEntry])
def get_agents_leaderboard(db: Session = Depends(get_db), limit: int = 20):
    return AgentService.leaderboard(db, limit=limit)


@router.get("/creator/stats", response_model=CreatorStatsResponse)
def get_creator_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AgentService.creator_stats(db, current_user.tenant_id, current_user.id)


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_owned_agent(db, current_user, agent_id)


@router.patch("/{agent_id}", response_model=AgentRead)
def update_agent(agent_id: UUID, payload: AgentUpdateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = _get_owned_agent(db, current_user, agent_id)
    AgentService.update_agent(agent, payload.model_dump(exclude_none=True))
    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = _get_owned_agent(db, current_user, agent_id)
    AgentService.delete_agent(db, agent)
    db.commit()
    return None


@router.post("/{agent_id}/run", response_model=AgentRunResponse)
def run_agent_endpoint(
    agent_id: UUID,
    payload: AgentRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    agent = _get_owned_agent(db, current_user, agent_id)
    log = AgentService.run_agent(db, agent, payload.input, current_user.id)
    db.commit()
    return AgentRunResponse(
        agent_id=agent.id,
        result=log.output_text or log.output_payload or "",
        tokens_used=int(log.tokens_used),
        execution_cost=float(log.execution_cost or log.tokens_consumed),
    )


@router.post("/{agent_id}/run-async", response_model=AgentAsyncRunResponse)
def run_agent_async_endpoint(
    agent_id: UUID,
    payload: AgentRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    agent = _get_owned_agent(db, current_user, agent_id)
    task = AgentService.enqueue_task(db, agent, payload.input, "manual_run")
    return AgentAsyncRunResponse(task_id=task.id, status=task.status)


@router.post("/{agent_id}/publish", response_model=AgentRead)
def publish_agent(
    agent_id: UUID,
    payload: AgentPublishRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    agent = _get_owned_agent(db, current_user, agent_id)
    try:
        AgentStoreService.publish_agent(
            db,
            agent,
            title=payload.title or agent.name,
            description=payload.description or agent.description,
            category=payload.category,
            tags=payload.tags,
            price_per_run=payload.price_per_run,
            price_per_month=payload.price_per_month,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    db.commit()
    db.refresh(agent)
    return agent


@router.post("/{agent_id}/unpublish", response_model=AgentRead)
def unpublish_agent(
    agent_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    agent = _get_owned_agent(db, current_user, agent_id)
    AgentStoreService.unpublish_agent(db, agent)
    db.commit()
    db.refresh(agent)
    return agent

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.agents.models import ManagedAgent
from app.modules.agents.schemas import AgentActionRequest, AgentCreateRequest, AgentRead
from app.modules.agents.service import AgentService

router = APIRouter()


def _get_owned_agent(db: Session, user_id: int, agent_id: UUID) -> ManagedAgent:
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id, ManagedAgent.owner_user_id == user_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent


@router.post("/create", response_model=AgentRead)
def create_agent(payload: AgentCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        agent = AgentService.create_agent(
            db,
            current_user.id,
            payload.name,
            payload.description,
            payload.strategy_type,
            payload.initial_capital,
        )
        db.commit()
        db.refresh(agent)
        return agent
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/start", response_model=AgentRead)
def start_agent(payload: AgentActionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = _get_owned_agent(db, current_user.id, payload.agent_id)
    AgentService.start_agent(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.post("/pause", response_model=AgentRead)
def pause_agent(payload: AgentActionRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = _get_owned_agent(db, current_user.id, payload.agent_id)
    AgentService.pause_agent(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return _get_owned_agent(db, current_user.id, agent_id)


@router.get("", response_model=list[AgentRead])
def list_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AgentService.list_agents(db, current_user.id)

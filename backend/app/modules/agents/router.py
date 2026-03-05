from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.agents.models import ManagedAgent
from app.modules.agents.schemas import AgentCreateRequest, AgentRead
from app.modules.agents.service import AgentService

router = APIRouter()


@router.post("/create", response_model=AgentRead)
def create_agent(payload: AgentCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        agent = AgentService.create_agent(db, current_user.id, payload.name, payload.description, payload.strategy_type)
        db.commit()
        db.refresh(agent)
        return agent
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("", response_model=list[AgentRead])
def list_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AgentService.list_agents(db, current_user.id)


@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id, ManagedAgent.owner_user_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    return agent


@router.post("/{agent_id}/start", response_model=AgentRead)
def start_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id, ManagedAgent.owner_user_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    try:
        AgentService.start_agent(db, agent)
        db.commit()
        db.refresh(agent)
        return agent
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/{agent_id}/stop", response_model=AgentRead)
def stop_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id, ManagedAgent.owner_user_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    AgentService.stop_agent(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id, ManagedAgent.owner_user_id == current_user.id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    AgentService.delete_agent(db, agent)
    db.commit()
    return None

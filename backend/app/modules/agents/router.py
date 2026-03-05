from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.agents.schemas import AgentCreateRequest, AgentRead, AgentUpdateRequest
from app.modules.agents.service import AgentService

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

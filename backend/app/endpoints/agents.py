from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.models import Agent
from app.schemas.agent import AgentCreate, AgentRead
from app.services.token_service import TOKEN_SERVICE

router = APIRouter()


@router.post("", response_model=AgentRead)
def create_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    TOKEN_SERVICE.burn_on_agent_creation(wallet="placeholder-wallet")
    agent = Agent(owner_id=1, **payload.model_dump())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent


@router.get("", response_model=list[AgentRead])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).order_by(Agent.id.desc()).all()

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.agents.models import AgentStoreListing, ManagedAgent
from app.modules.agents.runner import AgentRunner
from app.modules.agents.schemas import AgentReviewRead, AgentReviewRequest, InstallAgentResponse, StoreAgentRead
from app.modules.agents.store_service import AgentStoreService

router = APIRouter()


@router.get("/agents", response_model=list[StoreAgentRead])
def list_store_agents(
    category: str | None = None,
    price: float | None = Query(default=None, gt=0),
    rating: float | None = Query(default=None, ge=0, le=5),
    popularity: str = Query(default="trending"),
    db: Session = Depends(get_db),
):
    return AgentStoreService.list_store_agents(db, category=category, max_price=price, min_rating=rating, sort_by=popularity)


@router.get("/agents/{id}", response_model=StoreAgentRead)
def get_store_agent(id: int, db: Session = Depends(get_db)):
    listing = AgentStoreService.get_store_agent(db, id)
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store listing not found")
    return listing


@router.post("/install/{agent_id}", response_model=InstallAgentResponse)
def install_agent(agent_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id, ManagedAgent.is_published.is_(True)).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    listing = db.query(AgentStoreListing).filter(AgentStoreListing.agent_id == agent_id).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store listing not found")

    try:
        AgentStoreService.charge_for_install_run(db, user_id=current_user.id, agent=agent, listing=listing)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Token payment validation failed: {exc}") from exc

    installed = AgentStoreService.install_agent(db, user_id=current_user.id, agent_id=agent_id)
    AgentRunner.execute(db, agent=agent, caller_user_id=current_user.id)
    db.commit()
    db.refresh(installed)
    return installed


@router.get("/my-agents", response_model=list[InstallAgentResponse])
def my_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return AgentStoreService.my_agents(db, user_id=current_user.id)


@router.post("/review", response_model=AgentReviewRead)
def review_agent(payload: AgentReviewRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        review = AgentStoreService.add_review(
            db,
            agent_id=payload.agent_id,
            user_id=current_user.id,
            rating=payload.rating,
            review=payload.review,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    db.commit()
    db.refresh(review)
    return review


@router.get("/reviews/{agent_id}", response_model=list[AgentReviewRead])
def get_reviews(agent_id: UUID, db: Session = Depends(get_db)):
    return AgentStoreService.get_reviews(db, agent_id=agent_id)

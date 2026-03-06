from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import MarketplaceListing, User
from app.modules.agents.models import ManagedAgent
from app.modules.agents.runner import AgentRunner
from app.modules.notifications.service import NotificationService
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService

router = APIRouter()


class BuyAgentRequest(BaseModel):
    agent_id: UUID
    max_price: float = Field(gt=0)


@router.get("/agents")
def get_listings(db: Session = Depends(get_db)):
    return db.query(MarketplaceListing).filter(MarketplaceListing.active.is_(True)).order_by(MarketplaceListing.rating.desc()).all()


@router.post("/buy")
def buy_agent_service(payload: BuyAgentRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    listing = db.query(MarketplaceListing).filter(MarketplaceListing.agent_id == str(payload.agent_id), MarketplaceListing.active.is_(True)).first()
    if not listing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Listing not found")
    if listing.price_per_run > payload.max_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Listing price exceeds max_price")

    agent = db.query(ManagedAgent).filter(ManagedAgent.id == payload.agent_id).first()
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")

    buyer_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(current_user.id))
    agent_wallet = WalletService.get_wallet_by_id(db, agent.wallet_id)
    WalletService.transfer_tokens(db, buyer_wallet, agent_wallet, listing.price_per_run, tx_type=TransactionType.marketplace_purchase)

    AgentRunner.execute(db, agent, caller_user_id=current_user.id)
    listing.usage_count += 1

    NotificationService.create_notification(
        db,
        agent.owner_user_id,
        "Marketplace purchase",
        f"Your agent '{agent.name}' was purchased for {listing.price_per_run} AGC.",
    )
    NotificationService.create_notification(
        db,
        current_user.id,
        "Marketplace purchase completed",
        f"You purchased '{agent.name}' for {listing.price_per_run} AGC.",
    )
    db.commit()
    return {"status": "ok", "agent_id": str(agent.id), "price_paid": listing.price_per_run}

from __future__ import annotations

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import User
from app.modules.agents.models import AgentReview, AgentStoreListing, InstalledAgent, ManagedAgent
from app.modules.agents.schemas import AGENT_CATEGORIES
from app.modules.wallet.models import TransactionType, WalletOwnerType
from app.modules.wallet.service import WalletService


class AgentStoreService:
    @staticmethod
    def publish_agent(db: Session, agent: ManagedAgent, *, title: str, description: str | None, category: str, tags: list[str], price_per_run: float, price_per_month: float) -> AgentStoreListing:
        if category not in AGENT_CATEGORIES:
            raise ValueError("Invalid category")

        agent.is_public = True
        agent.is_published = True
        agent.category = category
        agent.tags = tags
        agent.price_per_run = price_per_run
        agent.price_per_month = price_per_month
        if description is not None:
            agent.description = description

        listing = db.query(AgentStoreListing).filter(AgentStoreListing.agent_id == agent.id).first()
        if listing:
            listing.title = title
            listing.description = description
            listing.category = category
            listing.price_per_run = price_per_run
            listing.price_per_month = price_per_month
        else:
            listing = AgentStoreListing(
                agent_id=agent.id,
                title=title,
                description=description,
                category=category,
                price_per_run=price_per_run,
                price_per_month=price_per_month,
                rating=agent.rating,
                usage_count=agent.total_runs,
            )
            db.add(listing)
        return listing

    @staticmethod
    def unpublish_agent(db: Session, agent: ManagedAgent) -> None:
        agent.is_published = False
        agent.is_public = False

    @staticmethod
    def list_store_agents(db: Session, *, category: str | None = None, max_price: float | None = None, min_rating: float | None = None, sort_by: str = "trending"):
        query = (
            db.query(AgentStoreListing, ManagedAgent, User)
            .join(ManagedAgent, ManagedAgent.id == AgentStoreListing.agent_id)
            .join(User, User.id == ManagedAgent.owner_user_id)
            .filter(ManagedAgent.is_published.is_(True), ManagedAgent.is_public.is_(True))
        )

        if category:
            query = query.filter(AgentStoreListing.category == category)
        if max_price is not None:
            query = query.filter(AgentStoreListing.price_per_run <= max_price)
        if min_rating is not None:
            query = query.filter(AgentStoreListing.rating >= min_rating)

        if sort_by == "new":
            query = query.order_by(AgentStoreListing.created_at.desc())
        elif sort_by == "top_rated":
            query = query.order_by(AgentStoreListing.rating.desc(), AgentStoreListing.usage_count.desc())
        else:
            trending_score = (AgentStoreListing.usage_count * 0.6) + (AgentStoreListing.rating * 0.4)
            query = query.order_by(trending_score.desc(), AgentStoreListing.created_at.desc())

        rows = query.all()
        return [
            {
                "id": listing.id,
                "agent_id": listing.agent_id,
                "title": listing.title,
                "description": listing.description,
                "category": listing.category,
                "price_per_run": float(listing.price_per_run),
                "price_per_month": float(listing.price_per_month),
                "rating": float(listing.rating),
                "usage_count": int(listing.usage_count),
                "created_at": listing.created_at,
                "creator_user_id": user.id,
                "creator_username": user.username,
                "total_runs": int(agent.total_runs or 0),
            }
            for listing, agent, user in rows
        ]

    @staticmethod
    def get_store_agent(db: Session, listing_id: int):
        row = (
            db.query(AgentStoreListing, ManagedAgent, User)
            .join(ManagedAgent, ManagedAgent.id == AgentStoreListing.agent_id)
            .join(User, User.id == ManagedAgent.owner_user_id)
            .filter(AgentStoreListing.id == listing_id, ManagedAgent.is_published.is_(True))
            .first()
        )
        if not row:
            return None
        listing, agent, user = row
        return {
            "id": listing.id,
            "agent_id": listing.agent_id,
            "title": listing.title,
            "description": listing.description,
            "category": listing.category,
            "price_per_run": float(listing.price_per_run),
            "price_per_month": float(listing.price_per_month),
            "rating": float(listing.rating),
            "usage_count": int(listing.usage_count),
            "created_at": listing.created_at,
            "creator_user_id": user.id,
            "creator_username": user.username,
            "total_runs": int(agent.total_runs or 0),
        }

    @staticmethod
    def install_agent(db: Session, *, user_id: int, agent_id):
        installed = db.query(InstalledAgent).filter(InstalledAgent.user_id == user_id, InstalledAgent.agent_id == agent_id).first()
        if installed:
            installed.active = True
            return installed
        installed = InstalledAgent(user_id=user_id, agent_id=agent_id, active=True)
        db.add(installed)
        db.flush()
        return installed

    @staticmethod
    def my_agents(db: Session, *, user_id: int):
        return (
            db.query(InstalledAgent)
            .filter(InstalledAgent.user_id == user_id, InstalledAgent.active.is_(True))
            .order_by(InstalledAgent.installed_at.desc())
            .all()
        )

    @staticmethod
    def charge_for_install_run(db: Session, *, user_id: int, agent: ManagedAgent, listing: AgentStoreListing) -> None:
        buyer_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(user_id))
        creator_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, str(agent.owner_user_id))
        treasury_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.treasury, "platform_treasury")
        infra_wallet = WalletService.get_or_create_wallet(db, WalletOwnerType.user, "agent_infra")

        amount = float(listing.price_per_run)
        creator_share = round(amount * 0.7, 4)
        treasury_share = round(amount * 0.2, 4)
        infra_share = round(amount - creator_share - treasury_share, 4)

        WalletService.transfer_tokens(db, buyer_wallet, creator_wallet, creator_share, tx_type=TransactionType.marketplace_purchase)
        WalletService.transfer_tokens(db, buyer_wallet, treasury_wallet, treasury_share, tx_type=TransactionType.marketplace_purchase)
        WalletService.transfer_tokens(db, buyer_wallet, infra_wallet, infra_share, tx_type=TransactionType.marketplace_purchase)

        listing.usage_count = int(listing.usage_count or 0) + 1
        agent.total_runs = int(agent.total_runs or 0) + 1
        agent.total_revenue = float(agent.total_revenue or 0) + amount

    @staticmethod
    def add_review(db: Session, *, agent_id, user_id: int, rating: int, review: str | None):
        existing = db.query(AgentReview).filter(AgentReview.agent_id == agent_id, AgentReview.user_id == user_id).first()
        if existing:
            raise ValueError("You already reviewed this agent")

        agent_review = AgentReview(agent_id=agent_id, user_id=user_id, rating=rating, review=review)
        db.add(agent_review)

        avg_rating = db.query(func.avg(AgentReview.rating)).filter(AgentReview.agent_id == agent_id).scalar()
        managed_agent = db.query(ManagedAgent).filter(ManagedAgent.id == agent_id).first()
        listing = db.query(AgentStoreListing).filter(AgentStoreListing.agent_id == agent_id).first()
        if managed_agent:
            managed_agent.rating = float(avg_rating or rating)
            managed_agent.average_rating = float(avg_rating or rating)
        if listing:
            listing.rating = float(avg_rating or rating)
        return agent_review

    @staticmethod
    def get_reviews(db: Session, *, agent_id):
        return (
            db.query(AgentReview)
            .filter(AgentReview.agent_id == agent_id)
            .order_by(AgentReview.created_at.desc())
            .all()
        )

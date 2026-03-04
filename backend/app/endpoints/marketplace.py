from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.models import MarketplaceListing

router = APIRouter()


@router.get("/listings")
def get_listings(db: Session = Depends(get_db)):
    return db.query(MarketplaceListing).filter(MarketplaceListing.active.is_(True)).all()

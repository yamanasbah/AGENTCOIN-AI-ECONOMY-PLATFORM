from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.modules.analytics.service import AnalyticsService

router = APIRouter()


@router.get("/platform")
def get_platform_analytics(db: Session = Depends(get_db)):
    return AnalyticsService.platform_stats(db)

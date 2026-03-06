from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.notifications.schemas import NotificationRead
from app.modules.notifications.service import NotificationService

router = APIRouter()


@router.get("", response_model=list[NotificationRead])
def get_notifications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return NotificationService.list_notifications(db, current_user.id)


@router.post("/read/{id}", response_model=NotificationRead)
def read_notification(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    notification = NotificationService.mark_as_read(db, current_user.id, id)
    if not notification:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    return notification

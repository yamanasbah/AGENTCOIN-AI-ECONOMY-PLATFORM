from sqlalchemy.orm import Session

from app.models.models import Notification


class NotificationService:
    @staticmethod
    def create_notification(db: Session, user_id: int, title: str, message: str) -> Notification:
        notification = Notification(user_id=user_id, title=title, message=message, read=False)
        db.add(notification)
        return notification

    @staticmethod
    def list_notifications(db: Session, user_id: int) -> list[Notification]:
        return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()

    @staticmethod
    def mark_as_read(db: Session, user_id: int, notification_id: int) -> Notification | None:
        item = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
        if item:
            item.read = True
            db.commit()
            db.refresh(item)
        return item

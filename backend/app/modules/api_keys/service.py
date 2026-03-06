import secrets

from sqlalchemy.orm import Session

from app.models.models import APIKey


class APIKeyService:
    @staticmethod
    def create_key(db: Session, user_id: int, name: str) -> APIKey:
        key = f"agc_{secrets.token_urlsafe(32)}"
        api_key = APIKey(user_id=user_id, key=key, name=name, is_active=True)
        db.add(api_key)
        db.commit()
        db.refresh(api_key)
        return api_key

    @staticmethod
    def list_keys(db: Session, user_id: int) -> list[APIKey]:
        return db.query(APIKey).filter(APIKey.user_id == user_id).order_by(APIKey.created_at.desc()).all()

    @staticmethod
    def delete_key(db: Session, user_id: int, key_id: int) -> bool:
        api_key = db.query(APIKey).filter(APIKey.id == key_id, APIKey.user_id == user_id).first()
        if not api_key:
            return False
        db.delete(api_key)
        db.commit()
        return True

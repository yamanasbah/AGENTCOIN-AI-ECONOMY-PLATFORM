from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.api_keys.schemas import APIKeyCreateRequest, APIKeyRead
from app.modules.api_keys.service import APIKeyService

router = APIRouter()


@router.post("/create", response_model=APIKeyRead)
def create_api_key(payload: APIKeyCreateRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return APIKeyService.create_key(db, current_user.id, payload.name)


@router.get("", response_model=list[APIKeyRead])
def list_api_keys(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return APIKeyService.list_keys(db, current_user.id)


@router.delete("/{id}")
def delete_api_key(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = APIKeyService.delete_key(db, current_user.id, id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    return {"status": "deleted"}

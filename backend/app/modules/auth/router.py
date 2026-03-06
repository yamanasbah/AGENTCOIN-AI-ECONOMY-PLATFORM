from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.models import User
from app.modules.auth.schemas import LoginRequest, RegisterRequest, TokenResponse, UserProfileResponse
from app.modules.auth.service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserProfileResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.register(db, payload.email, payload.username, payload.password)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    token = AuthService.login(db, payload.email, payload.password)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserProfileResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user

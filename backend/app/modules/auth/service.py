from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.models import User


class AuthService:
    @staticmethod
    def register(db: Session, email: str, username: str, password: str) -> User:
        existing = db.query(User).filter((User.email == email) | (User.username == username)).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already exists")

        user = User(
            email=email,
            username=username,
            password_hash=get_password_hash(password),
            tenant_id=f"tenant_{username.lower()}",
            is_admin=False,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def login(db: Session, email: str, password: str) -> str:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
        return create_access_token(str(user.id))

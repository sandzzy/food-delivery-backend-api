from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import auth as auth_crud
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token


def register_user(db: Session, data: RegisterRequest):
    existing = auth_crud.get_user_by_email(db, data.email)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return auth_crud.create_user(db, data)


def login_user(db: Session, data: LoginRequest) -> TokenResponse:
    user = auth_crud.get_user_by_email(db, data.email)
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return TokenResponse(access_token=token)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_admin
from app.schemas.user import UserResponse, UserUpdate
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return user_crud.get_all_users(db, skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return user_crud.get_user(db, user_id)


@router.put("/me", response_model=UserResponse)
def update_me(data: UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return user_crud.update_user(db, current_user, data)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    user = user_crud.get_user(db, user_id)
    user_crud.delete_user(db, user)
    return {"message": "User deleted"}

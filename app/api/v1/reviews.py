from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.review import ReviewCreate, ReviewResponse
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewResponse, status_code=201)
def create_review(data: ReviewCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return review_service.create_review(db, data, current_user)


@router.get("/{restaurant_id}", response_model=list[ReviewResponse])
def get_reviews(restaurant_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return review_service.get_restaurant_reviews(db, restaurant_id, skip, limit)

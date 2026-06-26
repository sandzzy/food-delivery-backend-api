from sqlalchemy.orm import Session
from app.models.review import Review
from app.schemas.review import ReviewCreate


def create_review(db: Session, data: ReviewCreate, user_id: int) -> Review:
    review = Review(**data.model_dump(), user_id=user_id)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_reviews_by_restaurant(db: Session, restaurant_id: int, skip: int = 0, limit: int = 10) -> list[Review]:
    return db.query(Review).filter(Review.restaurant_id == restaurant_id).offset(skip).limit(limit).all()

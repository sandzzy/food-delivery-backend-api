from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import review as review_crud
from app.crud import restaurant as restaurant_crud
from app.schemas.review import ReviewCreate
from app.models.user import User


def create_review(db: Session, data: ReviewCreate, user: User):
    restaurant = restaurant_crud.get_restaurant(db, data.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    review = review_crud.create_review(db, data, user.id)

    # Recalculate average rating
    reviews = review_crud.get_reviews_by_restaurant(db, data.restaurant_id, limit=10000)
    if reviews:
        restaurant.rating = round(sum(r.rating for r in reviews) / len(reviews), 2)
        db.commit()

    return review


def get_restaurant_reviews(db: Session, restaurant_id: int, skip: int, limit: int):
    return review_crud.get_reviews_by_restaurant(db, restaurant_id, skip, limit)

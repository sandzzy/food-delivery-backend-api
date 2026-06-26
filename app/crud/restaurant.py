from sqlalchemy.orm import Session
from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate


def get_restaurant(db: Session, restaurant_id: int) -> Restaurant | None:
    return db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()


def get_all_restaurants(db: Session, skip: int = 0, limit: int = 10) -> list[Restaurant]:
    return db.query(Restaurant).filter(Restaurant.status == True).offset(skip).limit(limit).all()


def create_restaurant(db: Session, data: RestaurantCreate, owner_id: int) -> Restaurant:
    restaurant = Restaurant(**data.model_dump(), owner_id=owner_id)
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def update_restaurant(db: Session, restaurant: Restaurant, data: RestaurantUpdate) -> Restaurant:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(restaurant, field, value)
    db.commit()
    db.refresh(restaurant)
    return restaurant


def delete_restaurant(db: Session, restaurant: Restaurant) -> None:
    db.delete(restaurant)
    db.commit()

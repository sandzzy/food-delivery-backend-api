from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from app.crud import restaurant as restaurant_crud
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.core.constants import Roles
from app.models.user import User
from app.utils.helpers import save_upload_file


def create_restaurant(db: Session, data: RestaurantCreate, owner: User):
    return restaurant_crud.create_restaurant(db, data, owner.id)


def update_restaurant(db: Session, restaurant_id: int, data: RestaurantUpdate, user: User):
    restaurant = restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if user.role != Roles.ADMIN and restaurant.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return restaurant_crud.update_restaurant(db, restaurant, data)


def delete_restaurant(db: Session, restaurant_id: int, user: User):
    restaurant = restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if user.role != Roles.ADMIN and restaurant.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    restaurant_crud.delete_restaurant(db, restaurant)
    return {"message": "Restaurant deleted"}


async def upload_restaurant_image(db: Session, restaurant_id: int, file: UploadFile, user: User):
    restaurant = restaurant_crud.get_restaurant(db, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")
    if user.role != Roles.ADMIN and restaurant.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    path = await save_upload_file(file, "restaurant_images")
    restaurant.image = path
    db.commit()
    db.refresh(restaurant)
    return restaurant

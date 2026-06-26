from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_restaurant_owner
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate, RestaurantResponse
from app.crud import restaurant as restaurant_crud
from app.services import restaurant_service

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=list[RestaurantResponse])
def list_restaurants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return restaurant_crud.get_all_restaurants(db, skip, limit)


@router.get("/{restaurant_id}", response_model=RestaurantResponse)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_crud.get_restaurant(db, restaurant_id)


@router.post("/", response_model=RestaurantResponse, status_code=201)
def create_restaurant(
    data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_restaurant_owner),
):
    return restaurant_service.create_restaurant(db, data, current_user)


@router.put("/{restaurant_id}", response_model=RestaurantResponse)
def update_restaurant(
    restaurant_id: int,
    data: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_restaurant_owner),
):
    return restaurant_service.update_restaurant(db, restaurant_id, data, current_user)


@router.delete("/{restaurant_id}")
def delete_restaurant(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_restaurant_owner),
):
    return restaurant_service.delete_restaurant(db, restaurant_id, current_user)


@router.post("/{restaurant_id}/image", response_model=RestaurantResponse)
async def upload_image(
    restaurant_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_restaurant_owner),
):
    return await restaurant_service.upload_restaurant_image(db, restaurant_id, file, current_user)

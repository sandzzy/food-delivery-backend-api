from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_restaurant_owner
from app.schemas.menu import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.crud import menu as menu_crud
from app.utils.helpers import save_upload_file

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/", response_model=list[MenuItemResponse])
def get_menu(restaurant_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return menu_crud.get_menu_by_restaurant(db, restaurant_id, skip, limit)


@router.post("/", response_model=MenuItemResponse, status_code=201)
def create_menu_item(
    data: MenuItemCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_restaurant_owner),
):
    return menu_crud.create_menu_item(db, data)


@router.put("/{item_id}", response_model=MenuItemResponse)
def update_menu_item(
    item_id: int,
    data: MenuItemUpdate,
    db: Session = Depends(get_db),
    _=Depends(get_current_restaurant_owner),
):
    item = menu_crud.get_menu_item(db, item_id)
    return menu_crud.update_menu_item(db, item, data)


@router.delete("/{item_id}")
def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_restaurant_owner),
):
    item = menu_crud.get_menu_item(db, item_id)
    menu_crud.delete_menu_item(db, item)
    return {"message": "Menu item deleted"}


@router.post("/{item_id}/image", response_model=MenuItemResponse)
async def upload_menu_image(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _=Depends(get_current_restaurant_owner),
):
    item = menu_crud.get_menu_item(db, item_id)
    path = await save_upload_file(file, "menu_images")
    item.image = path
    db.commit()
    db.refresh(item)
    return item

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.cart import CartItemAdd, CartItemUpdate, CartResponse
from app.services import cart_service

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=CartResponse)
def get_cart(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return cart_service.get_cart(db, current_user.id)


@router.post("/add")
def add_to_cart(data: CartItemAdd, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return cart_service.add_to_cart(db, current_user.id, data)


@router.put("/update")
def update_cart(data: CartItemUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return cart_service.update_cart(db, current_user.id, data)


@router.delete("/remove/{menu_item_id}")
def remove_from_cart(menu_item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return cart_service.remove_from_cart(db, current_user.id, menu_item_id)

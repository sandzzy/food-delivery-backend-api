from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import cart as cart_crud
from app.crud import menu as menu_crud
from app.schemas.cart import CartItemAdd, CartItemUpdate


def add_to_cart(db: Session, user_id: int, data: CartItemAdd):
    menu_item = menu_crud.get_menu_item(db, data.menu_item_id)
    if not menu_item or not menu_item.is_available:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found or unavailable")

    cart = cart_crud.get_or_create_cart(db, user_id)
    existing = cart_crud.get_cart_item(db, cart.id, data.menu_item_id)

    if existing:
        return cart_crud.update_cart_item(db, existing, existing.quantity + data.quantity)
    return cart_crud.add_cart_item(db, cart.id, data.menu_item_id, data.quantity)


def update_cart(db: Session, user_id: int, data: CartItemUpdate):
    cart = cart_crud.get_or_create_cart(db, user_id)
    item = cart_crud.get_cart_item(db, cart.id, data.menu_item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")
    if data.quantity <= 0:
        cart_crud.remove_cart_item(db, item)
        return {"message": "Item removed from cart"}
    return cart_crud.update_cart_item(db, item, data.quantity)


def remove_from_cart(db: Session, user_id: int, menu_item_id: int):
    cart = cart_crud.get_or_create_cart(db, user_id)
    item = cart_crud.get_cart_item(db, cart.id, menu_item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not in cart")
    cart_crud.remove_cart_item(db, item)
    return {"message": "Item removed from cart"}


def get_cart(db: Session, user_id: int):
    return cart_crud.get_or_create_cart(db, user_id)

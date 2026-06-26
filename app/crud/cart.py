from sqlalchemy.orm import Session
from app.models.cart import Cart, CartItem


def get_or_create_cart(db: Session, user_id: int) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def get_cart_item(db: Session, cart_id: int, menu_item_id: int) -> CartItem | None:
    return db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.menu_item_id == menu_item_id).first()


def add_cart_item(db: Session, cart_id: int, menu_item_id: int, quantity: int) -> CartItem:
    item = CartItem(cart_id=cart_id, menu_item_id=menu_item_id, quantity=quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_cart_item(db: Session, item: CartItem, quantity: int) -> CartItem:
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


def remove_cart_item(db: Session, item: CartItem) -> None:
    db.delete(item)
    db.commit()


def clear_cart(db: Session, cart_id: int) -> None:
    db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
    db.commit()

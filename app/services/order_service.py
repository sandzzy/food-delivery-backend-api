from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import order as order_crud
from app.crud import cart as cart_crud
from app.crud import coupon as coupon_crud
from app.schemas.order import OrderCreate
from app.core.constants import OrderStatus, Roles
from app.models.user import User


def place_order(db: Session, user_id: int, data: OrderCreate):
    cart = cart_crud.get_or_create_cart(db, user_id)
    if not cart.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")

    # Validate all items belong to the requested restaurant
    for item in cart.items:
        if item.menu_item.restaurant_id != data.restaurant_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item '{item.menu_item.name}' does not belong to this restaurant",
            )

    total = sum(item.menu_item.price * item.quantity for item in cart.items)
    coupon_id = None

    if data.coupon_code:
        coupon = coupon_crud.get_coupon_by_code(db, data.coupon_code)
        if not coupon or not coupon_crud.is_coupon_valid(coupon, total):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired coupon")
        total -= coupon.discount
        total = max(total, 0)
        coupon_id = coupon.id

    order = order_crud.create_order(db, user_id, data.restaurant_id, data.address_id, total, coupon_id)

    order_items = [
        {"menu_item_id": item.menu_item_id, "quantity": item.quantity, "price": item.menu_item.price}
        for item in cart.items
    ]
    order_crud.add_order_items(db, order.id, order_items)
    cart_crud.clear_cart(db, cart.id)

    return order_crud.get_order(db, order.id)


def get_user_orders(db: Session, user: User, skip: int, limit: int):
    if user.role == Roles.ADMIN:
        return db.query(__import__("app.models.order", fromlist=["Order"]).Order).offset(skip).limit(limit).all()
    return order_crud.get_orders_by_user(db, user.id, skip, limit)


def update_status(db: Session, user: User, order_id: int, new_status: str):
    valid_statuses = [
        OrderStatus.PENDING, OrderStatus.CONFIRMED, OrderStatus.PREPARING,
        OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED, OrderStatus.CANCELLED,
    ]
    if new_status not in valid_statuses:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order status")

    order = order_crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    # Customers can only cancel their own orders
    if user.role == Roles.CUSTOMER:
        if order.user_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        if new_status != OrderStatus.CANCELLED:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Customers can only cancel orders")

    return order_crud.update_order_status(db, order, new_status)

from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem


def create_order(db: Session, user_id: int, restaurant_id: int, address_id: int | None, total_amount: float, coupon_id: int | None = None) -> Order:
    order = Order(
        user_id=user_id,
        restaurant_id=restaurant_id,
        address_id=address_id,
        total_amount=total_amount,
        coupon_id=coupon_id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def add_order_items(db: Session, order_id: int, items: list[dict]) -> None:
    for item in items:
        order_item = OrderItem(order_id=order_id, **item)
        db.add(order_item)
    db.commit()


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 10) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()


def get_orders_by_restaurant(db: Session, restaurant_id: int, skip: int = 0, limit: int = 10) -> list[Order]:
    return db.query(Order).filter(Order.restaurant_id == restaurant_id).offset(skip).limit(limit).all()


def update_order_status(db: Session, order: Order, status: str) -> Order:
    order.order_status = status
    db.commit()
    db.refresh(order)
    return order

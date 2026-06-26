from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import payment as payment_crud
from app.crud import order as order_crud
from app.schemas.payment import PaymentCreate
from app.core.constants import PaymentStatus


def create_payment(db: Session, data: PaymentCreate, user_id: int):
    order = order_crud.get_order(db, data.order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    existing = payment_crud.get_payment_by_order(db, data.order_id)
    if existing and existing.payment_status == PaymentStatus.PAID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order already paid")

    payment = payment_crud.create_payment(db, data)
    # Simulate payment success (in production, integrate a real gateway)
    payment = payment_crud.mark_payment_paid(db, payment)
    order.payment_status = PaymentStatus.PAID
    db.commit()
    return payment


def get_payment(db: Session, order_id: int, user_id: int):
    order = order_crud.get_order(db, order_id)
    if not order or order.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    payment = payment_crud.get_payment_by_order(db, order_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment

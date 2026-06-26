from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate
from datetime import datetime
from app.core.constants import PaymentStatus


def create_payment(db: Session, data: PaymentCreate) -> Payment:
    payment = Payment(**data.model_dump())
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_payment_by_order(db: Session, order_id: int) -> Payment | None:
    return db.query(Payment).filter(Payment.order_id == order_id).first()


def mark_payment_paid(db: Session, payment: Payment) -> Payment:
    payment.payment_status = PaymentStatus.PAID
    payment.paid_at = datetime.utcnow()
    db.commit()
    db.refresh(payment)
    return payment

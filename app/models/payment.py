from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.core.constants import PaymentStatus, PaymentMethod


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    payment_method = Column(
        Enum(PaymentMethod.CASH, PaymentMethod.CARD, PaymentMethod.UPI, PaymentMethod.WALLET),
        nullable=False,
    )
    transaction_id = Column(String(150), nullable=True)
    payment_status = Column(
        Enum(PaymentStatus.PENDING, PaymentStatus.PAID, PaymentStatus.FAILED, PaymentStatus.REFUNDED),
        default=PaymentStatus.PENDING,
    )
    paid_at = Column(DateTime(timezone=True), nullable=True)

    order = relationship("Order", back_populates="payment")

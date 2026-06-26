from pydantic import BaseModel
from datetime import datetime


class PaymentCreate(BaseModel):
    order_id: int
    payment_method: str
    transaction_id: str | None = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    payment_method: str
    transaction_id: str | None
    payment_status: str
    paid_at: datetime | None

    class Config:
        from_attributes = True

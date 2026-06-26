from pydantic import BaseModel
from datetime import datetime


class OrderCreate(BaseModel):
    restaurant_id: int
    address_id: int | None = None
    coupon_code: str | None = None


class OrderStatusUpdate(BaseModel):
    order_id: int
    order_status: str


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    address_id: int | None
    total_amount: float
    payment_status: str
    order_status: str
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True

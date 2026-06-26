from pydantic import BaseModel
from datetime import date


class CouponCreate(BaseModel):
    code: str
    discount: float
    expiry_date: date
    minimum_order: float = 0.0


class CouponResponse(BaseModel):
    id: int
    code: str
    discount: float
    expiry_date: date
    minimum_order: float

    class Config:
        from_attributes = True

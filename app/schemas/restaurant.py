from pydantic import BaseModel
from datetime import time


class RestaurantCreate(BaseModel):
    name: str
    description: str | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    opening_time: time | None = None
    closing_time: time | None = None


class RestaurantUpdate(RestaurantCreate):
    status: bool | None = None


class RestaurantResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    description: str | None
    email: str | None
    phone: str | None
    address: str | None
    image: str | None
    opening_time: time | None
    closing_time: time | None
    rating: float
    status: bool

    class Config:
        from_attributes = True

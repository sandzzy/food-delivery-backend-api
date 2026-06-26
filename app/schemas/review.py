from pydantic import BaseModel, Field
from datetime import datetime


class ReviewCreate(BaseModel):
    restaurant_id: int
    rating: float = Field(..., ge=1, le=5)
    review: str | None = None


class ReviewResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    rating: float
    review: str | None
    created_at: datetime

    class Config:
        from_attributes = True

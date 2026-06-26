from pydantic import BaseModel


class CategoryCreate(BaseModel):
    restaurant_id: int
    name: str


class CategoryResponse(BaseModel):
    id: int
    restaurant_id: int
    name: str

    class Config:
        from_attributes = True

from pydantic import BaseModel


class MenuItemCreate(BaseModel):
    restaurant_id: int
    category_id: int | None = None
    name: str
    description: str | None = None
    price: float
    is_available: bool = True


class MenuItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    is_available: bool | None = None
    category_id: int | None = None


class MenuItemResponse(BaseModel):
    id: int
    restaurant_id: int
    category_id: int | None
    name: str
    description: str | None
    price: float
    image: str | None
    is_available: bool

    class Config:
        from_attributes = True

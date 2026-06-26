from pydantic import BaseModel
from app.schemas.menu import MenuItemResponse


class CartItemAdd(BaseModel):
    menu_item_id: int
    quantity: int = 1


class CartItemUpdate(BaseModel):
    menu_item_id: int
    quantity: int


class CartItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    menu_item: MenuItemResponse

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItemResponse]

    class Config:
        from_attributes = True

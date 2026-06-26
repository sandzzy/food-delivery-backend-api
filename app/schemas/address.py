from pydantic import BaseModel


class AddressCreate(BaseModel):
    house_no: str | None = None
    street: str | None = None
    city: str
    state: str
    pincode: str


class AddressResponse(BaseModel):
    id: int
    user_id: int
    house_no: str | None
    street: str | None
    city: str
    state: str
    pincode: str

    class Config:
        from_attributes = True

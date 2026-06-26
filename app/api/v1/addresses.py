from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.address import AddressCreate, AddressResponse
from app.models.address import Address

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/", response_model=list[AddressResponse])
def list_addresses(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Address).filter(Address.user_id == current_user.id).all()


@router.post("/", response_model=AddressResponse, status_code=201)
def create_address(data: AddressCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    address = Address(**data.model_dump(), user_id=current_user.id)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    address = db.query(Address).filter(Address.id == address_id, Address.user_id == current_user.id).first()
    db.delete(address)
    db.commit()
    return {"message": "Address deleted"}

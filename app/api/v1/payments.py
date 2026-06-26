from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.services import payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentResponse, status_code=201)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return payment_service.create_payment(db, data, current_user.id)


@router.get("/{order_id}", response_model=PaymentResponse)
def get_payment(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return payment_service.get_payment(db, order_id, current_user.id)

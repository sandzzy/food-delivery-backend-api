from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user
from app.schemas.coupon import CouponCreate, CouponResponse
from app.services import coupon_service

router = APIRouter(prefix="/coupons", tags=["Coupons"])


@router.post("/", response_model=CouponResponse, status_code=201)
def create_coupon(data: CouponCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return coupon_service.create_coupon(db, data)


@router.get("/", response_model=list[CouponResponse])
def list_coupons(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return coupon_service.get_all_coupons(db)

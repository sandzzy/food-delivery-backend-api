from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import coupon as coupon_crud
from app.schemas.coupon import CouponCreate


def create_coupon(db: Session, data: CouponCreate):
    existing = coupon_crud.get_coupon_by_code(db, data.code)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Coupon code already exists")
    return coupon_crud.create_coupon(db, data)


def get_all_coupons(db: Session):
    return coupon_crud.get_all_coupons(db)


def validate_coupon(db: Session, code: str, order_total: float):
    coupon = coupon_crud.get_coupon_by_code(db, code)
    if not coupon or not coupon_crud.is_coupon_valid(coupon, order_total):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired coupon")
    return coupon

from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.schemas.coupon import CouponCreate
from datetime import date


def create_coupon(db: Session, data: CouponCreate) -> Coupon:
    coupon = Coupon(**data.model_dump())
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon


def get_coupon_by_code(db: Session, code: str) -> Coupon | None:
    return db.query(Coupon).filter(Coupon.code == code).first()


def get_all_coupons(db: Session) -> list[Coupon]:
    return db.query(Coupon).filter(Coupon.expiry_date >= date.today()).all()


def is_coupon_valid(coupon: Coupon, order_total: float) -> bool:
    return coupon.expiry_date >= date.today() and order_total >= coupon.minimum_order

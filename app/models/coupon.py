from sqlalchemy import Column, Integer, String, Float, Date
from app.core.database import Base


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    discount = Column(Float, nullable=False)
    expiry_date = Column(Date, nullable=False)
    minimum_order = Column(Float, default=0.0)

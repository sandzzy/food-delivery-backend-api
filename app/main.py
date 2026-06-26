from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.database import Base, engine
from app.middleware.logging import log_requests

# Import all models so SQLAlchemy registers them before create_all
from app.models import user, restaurant, category, menu, cart, order, order_item, address, payment, review, coupon  # noqa

# Import routers
from app.api.v1 import auth, users, restaurants, categories, menu as menu_router
from app.api.v1 import cart as cart_router, orders, payments, reviews, coupons, addresses

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="🍔 Food Delivery API",
    description="A full-featured food delivery backend built with FastAPI + MySQL",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

# Routers
PREFIX = "/api/v1"
app.include_router(auth.router, prefix=PREFIX)
app.include_router(users.router, prefix=PREFIX)
app.include_router(restaurants.router, prefix=PREFIX)
app.include_router(categories.router, prefix=PREFIX)
app.include_router(menu_router.router, prefix=PREFIX)
app.include_router(cart_router.router, prefix=PREFIX)
app.include_router(orders.router, prefix=PREFIX)
app.include_router(payments.router, prefix=PREFIX)
app.include_router(reviews.router, prefix=PREFIX)
app.include_router(coupons.router, prefix=PREFIX)
app.include_router(addresses.router, prefix=PREFIX)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Food Delivery API is running 🚀"}

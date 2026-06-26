from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, get_current_restaurant_owner
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=201)
def place_order(data: OrderCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return order_service.place_order(db, current_user.id, data)


@router.get("/", response_model=list[OrderResponse])
def list_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return order_service.get_user_orders(db, current_user, skip, limit)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    from app.crud import order as order_crud
    from fastapi import HTTPException, status
    order = order_crud.get_order(db, order_id)
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/status")
def update_order_status(
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_restaurant_owner),
):
    return order_service.update_status(db, current_user, data.order_id, data.order_status)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_restaurant_owner
from app.schemas.category import CategoryCreate, CategoryResponse
from app.models.category import Category

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{restaurant_id}", response_model=list[CategoryResponse])
def get_categories(restaurant_id: int, db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.restaurant_id == restaurant_id).all()


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
    _=Depends(get_current_restaurant_owner),
):
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _=Depends(get_current_restaurant_owner),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}

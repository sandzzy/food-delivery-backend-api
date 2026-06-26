from sqlalchemy.orm import Session
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemUpdate


def get_menu_item(db: Session, item_id: int) -> MenuItem | None:
    return db.query(MenuItem).filter(MenuItem.id == item_id).first()


def get_menu_by_restaurant(db: Session, restaurant_id: int, skip: int = 0, limit: int = 50) -> list[MenuItem]:
    return (
        db.query(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_menu_item(db: Session, data: MenuItemCreate) -> MenuItem:
    item = MenuItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_menu_item(db: Session, item: MenuItem, data: MenuItemUpdate) -> MenuItem:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


def delete_menu_item(db: Session, item: MenuItem) -> None:
    db.delete(item)
    db.commit()

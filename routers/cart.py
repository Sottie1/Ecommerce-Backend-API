from fastapi import APIRouter
from app.database import SessionLocal
from app.models import CartItem
from app.schemas import CartItemCreate
from sqlalchemy.orm import Session
from fastapi import Depends
from app import schemas, models
from app.dependency import get_db

router = APIRouter()

@router.post("/api/v1/cart")
def add_to_cart(cart_item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = models.CartItem(user_id=cart_item.user_id, product_id=cart_item.product_id, quantity=cart_item.quantity)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item
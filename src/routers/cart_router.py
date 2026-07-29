from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.crud.cart_crud import add_to_cart, remove_from_cart, get_cart
from src.schemas.cart_schema import CartItemCreate
from src.auth.jwt_handler import get_current_user
from src.database import SessionLocal

router = APIRouter()


@router.post("/cart/add")
def add_item(item: CartItemCreate, db: Session = Depends(SessionLocal), user: str = Depends(get_current_user)):
    return add_to_cart(db=db, user_id=user.id, item=item)


@router.delete("/cart/remove/{item_id}")
def remove_item(item_id: int, db: Session = Depends(SessionLocal), user: str = Depends(get_current_user)):
    return remove_from_cart(db=db, user_id=user.id, item_id=item_id)


@router.get("/cart")
def view_cart(db: Session = Depends(SessionLocal), user: str = Depends(get_current_user)):
    return get_cart(db=db, user_id=user.id)
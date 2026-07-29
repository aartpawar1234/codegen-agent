from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.crud.order_crud import create_order, get_order, get_user_orders
from src.auth.jwt_handler import get_current_user
from src.database import SessionLocal

router = APIRouter()


@router.post("/checkout")
def checkout(db: Session = Depends(SessionLocal), user: str = Depends(get_current_user)):
    return create_order(db=db, user_id=user.id)


@router.get("/orders/{id}")
def read_order(id: int, db: Session = Depends(SessionLocal), user: str = Depends(get_current_user)):
    return get_order(db=db, order_id=id)


@router.get("/orders")
def list_orders(db: Session = Depends(SessionLocal), user: str = Depends(get_current_user)):
    return get_user_orders(db=db, user_id=user.id)
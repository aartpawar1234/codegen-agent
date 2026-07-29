from sqlalchemy.orm import Session
from src.models.order_model import Order, OrderItem
from src.schemas.order_schema import OrderResponse
from src.crud.cart_crud import get_cart


def create_order(db: Session, user_id: int):
    cart_items = get_cart(db, user_id)
    if not cart_items:
        return None
    total_amount = sum(item.quantity * item.price_at_purchase for item in cart_items)
    order = Order(user_id=user_id, total_amount=total_amount)
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in cart_items:
        order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price_at_purchase=item.price_at_purchase)
        db.add(order_item)
    db.commit()
    return order


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()
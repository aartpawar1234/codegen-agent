from sqlalchemy.orm import Session
from src.models.cart_model import Cart, CartItem
from src.schemas.cart_schema import CartItemCreate
from src.crud.product_crud import get_product


def add_to_cart(db: Session, user_id: int, item: CartItemCreate):
    product = get_product(db, item.product_id)
    if product and product.stock_quantity >= item.quantity:
        cart = db.query(Cart).filter(Cart.user_id == user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        cart_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        return cart_item
    return None


def remove_from_cart(db: Session, user_id: int, item_id: int):
    cart_item = db.query(CartItem).filter(CartItem.id == item_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return cart_item
    return None


def get_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart:
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        return items
    return []


def clear_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if cart:
        db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
        db.commit()
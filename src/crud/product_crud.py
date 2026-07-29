from sqlalchemy.orm import Session
from src.models.product_model import Product
from src.schemas.product_schema import ProductCreate


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, category: str = None):
    if category:
        return db.query(Product).filter(Product.category == category).all()
    return db.query(Product).all()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
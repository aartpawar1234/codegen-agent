from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.crud.product_crud import get_product, get_products, create_product
from src.schemas.product_schema import ProductCreate, ProductResponse
from src.auth.jwt_handler import get_current_admin
from src.database import SessionLocal

router = APIRouter()


@router.get("/products", response_model=list[ProductResponse])
def list_products(category: str = None, db: Session = Depends(SessionLocal)):
    return get_products(db=db, category=category)


@router.get("/products/{id}", response_model=ProductResponse)
def read_product(id: int, db: Session = Depends(SessionLocal)):
    return get_product(db=db, product_id=id)


@router.post("/products", response_model=ProductResponse, dependencies=[Depends(get_current_admin)])
def add_product(product: ProductCreate, db: Session = Depends(SessionLocal)):
    return create_product(db=db, product=product)
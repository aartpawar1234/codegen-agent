from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(CartItemCreate):
    id: int

class CartResponse(BaseModel):
    items: list[CartItemResponse]
    total_price: float

    class Config:
        orm_mode = True
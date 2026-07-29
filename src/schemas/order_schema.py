from pydantic import BaseModel

class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    items: list[OrderItemResponse]

    class Config:
        orm_mode = True
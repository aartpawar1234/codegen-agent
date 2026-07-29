from fastapi import FastAPI
from src.routers import products_router, cart_router, orders_router, auth_router

app = FastAPI()

app.include_router(products_router.router)
app.include_router(cart_router.router)
app.include_router(orders_router.router)
app.include_router(auth_router.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
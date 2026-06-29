from fastapi import FastAPI
from .routers import auth
from .database import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the JWT Authentication API"}

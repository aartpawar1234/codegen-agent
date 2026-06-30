from fastapi import FastAPI
from .routers import auth
from .database.session import engine, Base

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

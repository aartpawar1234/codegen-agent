from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(auth_router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the JWT Authentication API"}
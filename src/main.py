"""
FastAPI application setup and inclusion of routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import auth
from src.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="JWT Authentication API",
    description="API for JWT authentication with login, logout, and refresh endpoints",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "JWT Authentication API"}

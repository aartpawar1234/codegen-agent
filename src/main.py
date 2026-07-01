from fastapi import FastAPI, Request
from .database import engine, SessionLocal
from . import models
from .auth.router import router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def add_db_session(request: Request, call_next):
    response = None
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

app.include_router(router)

# Ensure the app is running correctly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

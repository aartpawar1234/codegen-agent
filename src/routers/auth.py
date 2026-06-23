from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, auth
from ..database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=schemas.LoginResponse)
async def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, request.email)
    if not user or not user.hashed_password == request.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = auth.create_access_token(user.email)
    refresh_token = auth.create_refresh_token(user.email)
    return schemas.LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout(request: schemas.LogoutRequest, db: Session = Depends(get_db)):
    crud.revoke_token(db, request.refresh_token)
    return {"msg": "Successfully logged out"}


@router.post("/refresh", response_model=schemas.RefreshResponse)
async def refresh(request: schemas.RefreshRequest, db: Session = Depends(get_db)):
    if crud.is_token_revoked(db, request.refresh_token):
        raise HTTPException(status_code=400, detail="Token has been revoked")
    email = auth.decode_token(request.refresh_token)["sub"]
    access_token = auth.create_access_token(email)
    return schemas.RefreshResponse(access_token=access_token)
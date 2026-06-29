from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src import schemas, crud
from src.utils import security
from src.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(data={"sub": user.email})
    refresh_token = security.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/logout")
async def logout(token: str, db: Session = Depends(get_db)):
    crud.add_token_to_blacklist(db, token)
    return {"msg": "Successfully logged out"}

@router.post("/refresh", response_model=schemas.Token)
async def refresh(token: str, db: Session = Depends(get_db)):
    if crud.is_token_blacklisted(db, token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is blacklisted")
    payload = security.verify_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    access_token = security.create_access_token(data={"sub": payload["sub"]})
    crud.add_token_to_blacklist(db, token)  # Blacklist the refresh token
    return {"access_token": access_token, "token_type": "bearer"}

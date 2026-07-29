from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.crud.user_crud import register_user, authenticate_user
from src.schemas.user_schema import UserCreate, UserLogin, Token
from src.auth.jwt_handler import create_access_token
from src.database import SessionLocal

router = APIRouter()


@router.post("/register", response_model=UserCreate)
def register(user: UserCreate, db: Session = Depends(SessionLocal)):
    return register_user(db=db, user=user)


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(SessionLocal)):
    db_user = authenticate_user(db=db, username=user.username, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
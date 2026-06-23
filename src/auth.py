import jwt
from datetime import datetime, timedelta
from .config import settings
from .schemas import LoginResponse


def create_access_token(email: str) -> str:
    expiration = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION)
    token = jwt.encode({"sub": email, "exp": expiration}, settings.JWT_SECRET, algorithm="HS256")
    return token


def create_refresh_token(email: str) -> str:
    expiration = datetime.utcnow() + timedelta(days=30)
    token = jwt.encode({"sub": email, "exp": expiration}, settings.JWT_SECRET, algorithm="HS256")
    return token


def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])


def verify_token(token: str) -> bool:
    try:
        decode_token(token)
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
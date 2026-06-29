from sqlalchemy.orm import Session
from src import models


def add_token_to_blacklist(db: Session, token: str) -> models.TokenBlacklist:
    db_token = models.TokenBlacklist(token=token)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(models.TokenBlacklist).filter(models.TokenBlacklist.token == token).first() is not None


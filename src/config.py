import os

class Settings:
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your_jwt_secret")
    JWT_EXPIRATION: int = int(os.getenv("JWT_EXPIRATION", 3600))  # 1 hour
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

settings = Settings()
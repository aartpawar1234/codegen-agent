from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite:///./todos.db"

settings = Settings()

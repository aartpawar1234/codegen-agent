"""
Configuration settings for JWT, database, and application.
Uses environment variables for sensitive configurations.
"""

from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, SecretStr


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # JWT settings
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Rate limiting
    LOGIN_RATE_LIMIT: int = 5  # Max attempts per minute

    @property
    def database_url(self) -> str:
        """Construct PostgreSQL connection URL."""
        password = self.POSTGRES_PASSWORD.get_secret_value()
        return PostgresDsn.build(
            scheme="postgresql",
            username=self.POSTGRES_USER,
            password=password,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()

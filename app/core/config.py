from functools import lru_cache
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from urllib.parse import quote


class Settings(BaseSettings):
    ENV: str = "dev"
    DEBUG: bool = False
    PROJECT_NAME: str = "MyService"
    API_V1_PREFIX: str = "/api/v1"
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str = "HS256"

    # security
    SECRET_KEY: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_PASSWORD: str
    ALLOWED_ORIGINS: list[AnyHttpUrl] = []

    # db example
    DATABASE_URL: str | None = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # URL encode password in case it contains special chars like @
        password_encoded = quote(self.DB_PASSWORD)
        return f"postgresql+psycopg://{self.DB_USER}:{password_encoded}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

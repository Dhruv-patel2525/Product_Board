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
    # DB_USER: str
    DB_HOST: str
    DB_PORT: str
    # DB_NAME: str
    # DB_PASSWORD: str
    POSTGRES_DB:str
    POSTGRES_USER:str 
    POSTGRES_PASSWORD:str

    ALLOWED_ORIGINS: list[AnyHttpUrl] = []

    REDIS_URL:str
    CELERY_BROKER_URL:str
    CELERY_RESULT_BACKEND:str

    # FastAPI
    FRONTEND_URL:str
    SMTP_PASSWORD:str
    SMTP_HOST :str
    SMTP_PORT:int
    SMTP_USER :str
    FROM_EMAIL:str

    # db example
    DATABASE_URL: str | None = None

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # URL encode password in case it contains special chars like @
        password_encoded = quote(self.POSTGRES_PASSWORD)
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{password_encoded}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

settings=get_settings()

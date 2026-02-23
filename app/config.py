from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    ALLOCATION_STRATEGY: Literal["pulp", "greedy"] = "pulp"

    class Config:
        env_file = ".env"

settings = Settings()


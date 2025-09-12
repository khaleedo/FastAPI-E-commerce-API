from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    secret_key: str = "your-super-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "postgresql://postgres:Amogah@localhost:5432/fastapi_db"

    class Config:
        env_file = ".env"


settings = Settings()
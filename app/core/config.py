from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    APP_TITLE: str = 'Куаркот'
    DESCRIPTION: str = 'Жертвуй всем'
    DATABASE_URL: str = 'sqlite+aiosqlite:///./fastapi.db'
    SECRET: str = 'SECRET'

    FIRST_SUPERUSER_EMAIL: Optional[EmailStr] = None
    FIRST_SUPERUSER_PASSWORD: Optional[str] = None

    ZERO: int = 0
    LENGTH_NAME: int = 100
    MIN_ANYSTR_LENGTH: int = 1
    MIN_LENGTH_PASS: int = 3
    LIFETIME_JWT: int = 3600

    class Config:
        env_file = '.env'


settings = Settings()

from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Куаркот'
    description: str = 'Жертвуй всем'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    zero: int = 0
    length_name: int = 100
    min_anystr_length: int = 1
    min_length_pass: int = 3
    lifetime_jwt: int = 3600

    class Config:
        env_file = '.env'


settings = Settings()

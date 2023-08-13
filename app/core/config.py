from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Куаркот'
    description: str = 'Жертвуй всем'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    length_name: int = None
    min_anystr_length: int = None
    min_length_pass: int = None
    zero: int = None
    lifetime_jwt: int = None

    class Config:
        env_file = '.env'


settings = Settings()

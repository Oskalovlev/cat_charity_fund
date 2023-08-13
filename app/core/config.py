from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Куаркот'
    description: str = 'Жертвуй всем'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    zero: int
    length_name: int
    min_anystr_length: int
    min_length_pass: int
    lifetime_jwt: int

    class Config:
        env_file = '.env'


settings = Settings()

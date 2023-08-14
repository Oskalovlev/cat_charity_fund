from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field, Extra, PositiveInt, validator

from app.core.config import settings


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=settings.LENGTH_NAME)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = settings.MIN_ANYSTR_LENGTH


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(max_length=settings.LENGTH_NAME)
    description: str = Field()
    full_amount: PositiveInt = Field()

    class Config:
        min_anystr_length = settings.MIN_ANYSTR_LENGTH


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_is_not_none(cls, value):
        if value is None:
            raise ValueError('Имя не может отсутсвовать')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field()
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
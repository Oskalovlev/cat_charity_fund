from datetime import datetime

from typing import Optional

from pydantic import BaseModel, PositiveInt, Field


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    user_id: int
    invested_amount: int = Field()
    fully_invested: bool
    close_date: Optional[datetime]

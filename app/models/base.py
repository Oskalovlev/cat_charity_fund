from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Boolean, CheckConstraint

from app.core.db import Base
from app.core.config import settings


class BaseModel(Base):

    __abstract__ = True

    __table_agrs__ = (
        CheckConstraint(f'full_amount > {settings.ZERO}'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=settings.ZERO)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
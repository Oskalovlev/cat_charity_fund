from sqlalchemy import ForeignKey, Column, Text, Integer

from app.models.base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

from sqlalchemy import Column, String, Text

from app.models.base import BaseModel
from app.core.config import settings


class CharityProject(BaseModel):
    name = Column(String(settings.length_name), unique=True, nullable=False)
    description = Column(Text, nullable=False)

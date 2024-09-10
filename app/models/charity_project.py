from sqlalchemy import Column, String, Text

from .base import BaseModel
from app.core.constants import CHARITY_PROJECT_NAME_MAX_LEN


class CharityProject(BaseModel):
    name = Column(
        String(CHARITY_PROJECT_NAME_MAX_LEN), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)

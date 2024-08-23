from sqlalchemy import Column, String, Text

from .base import BaseModel
from app.core.constants import charity_project_name_max_len


class CharityProject(BaseModel):
    name = Column(
        String(charity_project_name_max_len), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)

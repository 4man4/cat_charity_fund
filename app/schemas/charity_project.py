from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, Extra


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = 1


# class CharityProjectCreate(CharityProjectBase):
class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    class Config:
        min_anystr_length = 1


class CharityProjectUpdate(CharityProjectBase):
    pass


#     @validator('name')
#     def validate_name(cls, value):
#         if value is None:
#             raise ValueError('Название переговорки не может быть пустым')
#         return value


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt, Extra

from app.core.constants import (
    CHARITY_PROJECT_NAME_MAX_LEN,
    INVESTED_AMOUNT_DEFAULT,
    CHARITY_PROJECT_MIN_ANYSTR_LEN,
)


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=CHARITY_PROJECT_NAME_MAX_LEN)
    description: Optional[str] = Field(None)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid
        min_anystr_length = CHARITY_PROJECT_MIN_ANYSTR_LEN


class CharityProjectCreate(BaseModel):
    name: str = Field(..., max_length=CHARITY_PROJECT_NAME_MAX_LEN)
    description: str = Field(...)
    full_amount: PositiveInt = Field(...)

    class Config:
        min_anystr_length = CHARITY_PROJECT_MIN_ANYSTR_LEN


class CharityProjectUpdate(CharityProjectBase):
    pass


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(INVESTED_AMOUNT_DEFAULT)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True

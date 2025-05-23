from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field

from app.core.constants import INVESTED_AMOUNT_DEFAULT


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationCreate):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int = Field(INVESTED_AMOUNT_DEFAULT)
    fully_invested: bool
    close_date: Optional[datetime]

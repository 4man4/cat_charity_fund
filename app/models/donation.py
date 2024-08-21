from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from .base import BaseModel


class Donation(BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)

    # def __repr__(self):
    #     return f'Уже забронировано с {self.from_reserve} по {self.to_reserve}'

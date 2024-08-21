# from sqlalchemy import Column, Integer
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    # id = Column(Integer, primary_key=True)
    pass
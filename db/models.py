# src/models.py
from sqlalchemy import Column, Integer, String
from .db import Base

class User(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)

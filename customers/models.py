from sqlalchemy import Column, Integer, String, CHAR, Date, Enum
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from datetime import datetime
from . import enum

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer,nullable=False,primary_key=True)
    name = Column(String,nullable=False)
    sex : enum.SexEnum = Column(Enum(enum.SexEnum),nullable=True)
    birth_date = Column(Date,nullable=True)
    created_at = Column(TIMESTAMP(timezone=False),server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=False),server_default=text("now()"),onupdate=text("now()"))

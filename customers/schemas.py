from . import enum
from pydantic import BaseModel
from typing import Optional
from datetime import date


class Customers(BaseModel):
    name: str
    sex: Optional[enum.SexEnum] = enum.SexEnum.DiversOrOpen
    birth_date : date

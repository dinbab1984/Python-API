from . import enum
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime

class Users(BaseModel):
    email: EmailStr
    password: str
        
class UsersResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    class ConfigDict:
        from_attributes = True

class Customers(BaseModel):
    name: str
    sex: Optional[enum.SexEnum] = enum.SexEnum.DiversOrOpen
    birth_date : date
        
class CustomersReponse(Customers):
    id: int
    created_at: datetime
    created_user: UsersResponse
    class ConfigDict:
        from_attributes = True

class Login(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str


        
        


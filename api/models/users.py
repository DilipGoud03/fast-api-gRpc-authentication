from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserLogin(BaseModel):
    email: EmailStr
    password: str

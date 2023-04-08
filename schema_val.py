from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Review Validation


class Review_Req(BaseModel):
    desc: str
    rating: int


class Review_Res(BaseModel):
    desc: Optional[str]
    rating: Optional[int]
    user_id: Optional[int]
    item_id: Optional[int]

    class Config:
        orm_mode = True


# User Schema Validation

class User_Req(BaseModel):
    user_name: str
    email: EmailStr
    password: str


class Login_Req(BaseModel):
    email: EmailStr
    password: str


class User_Res(BaseModel):
    user_id: int
    user_name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Item Schema Validation

class Item_Req(BaseModel):
    name: str
    price: float
    inventory: int
    desc: str


class Item_Res(Item_Req):
    item_id: int
    created_at: datetime
    user_id: int
    owner: User_Res
    review: Optional[Review_Res]

    class Config:
        orm_mode = True


# Token Validation
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None

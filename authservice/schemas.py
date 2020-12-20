from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    access_token: str
    exp: Optional[int]
    sub: Optional[str]
    blacklisted: Optional[bool]
    user_id: Optional[str]


class Token(TokenBase):
    id: int

    class Config:
        orm_mode = True


class TokenCreate(TokenBase):
    pass


class TokenData(BaseModel):
    username: Optional[str] = None

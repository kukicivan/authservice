from typing import List, Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class TokenBase(BaseModel):
    access_token: str
    expires_at: Optional[int]
    refresh_token: Optional[str]

    # Token
    blacklisted: Optional[bool]

    # Token properties
    token_data: Optional[str]


class Token(TokenBase):
    id: int

    class Config:
        orm_mode = True


class TokenCreate(TokenBase):
    pass

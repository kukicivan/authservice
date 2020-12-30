from typing import Optional

from pydantic import BaseModel, EmailStr, UUID4


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID4
    is_active: Optional[bool]

    class Config:
        orm_mode = True

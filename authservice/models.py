from fastapi_users import models
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)

    # Token
    access_token = Column(String(length=1024), nullable=False)
    expires_at = Column(Integer, nullable=True)
    refresh_token = Column(String(length=1024), nullable=True)

    # Token properties
    blacklisted = Column(Boolean, default=False, nullable=True)

    # Token data and user info
    token_data: Column(String(length=1024), nullable=True)

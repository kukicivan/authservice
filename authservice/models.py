from typing import Any

import databases
from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import relationship

from authservice.database import SQLALCHEMY_DATABASE_URL

# Declarative base to register SQLAlchemy models
Base: DeclarativeMeta = declarative_base()


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, index=True)

    access_token = Column(String(length=1024), nullable=False)
    exp = Column(Integer, nullable=True)
    sub = Column(String(length=1024), nullable=True)
    blacklisted = Column(Boolean, default=False)

    user_id = Column(String(length=1024), nullable=True)
    # user_id = Column(String(length=1024), ForeignKey('user.id'))
    # user = relationship("user", back_populates='token')


def migrate(engine: Any):
    """
        Database migration adapter for SQLAlchemy.

       :param engine: `Any` instance from `SQLAlchemyEngine`.
        """

    database = databases.Database(SQLALCHEMY_DATABASE_URL)

    users = UserTable.__table__
    user_db = SQLAlchemyUserDatabase(UserDB, database, users)

    # Create all table in database
    Base.metadata.create_all(bind=engine)

    return user_db

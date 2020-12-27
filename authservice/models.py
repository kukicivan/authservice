from typing import Any

from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

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


# Create all table in database
def migrate(db: Any):
    """
        Database migration adapter for SQLAlchemy.

       :param db: `Any` instance from `SQLAlchemyEngine`.
        """
    Base.metadata.create_all(bind=db)

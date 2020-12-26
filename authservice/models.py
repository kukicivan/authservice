from typing import Any

import databases
from fastapi_users import models
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

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

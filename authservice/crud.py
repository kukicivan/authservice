from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from . import models


async def get_users(db: Any, skip: int = 0, limit: int = 100) -> object:
    # Fetch multiple rows
    query = "SELECT * FROM user"
    rows = await db.fetch_all(query=query)
    return rows


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.UserTable).filter(models.UserTable.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserTable).filter(models.UserTable.email == email).first()

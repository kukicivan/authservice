from sqlalchemy.orm import Session

from . import models


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserTable).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.UserTable).filter(models.UserTable.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserTable).filter(models.UserTable.email == email).first()

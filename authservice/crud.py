from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.UserTable).filter(models.UserTable.email == email).first()


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.UserTable).filter(models.UserTable.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.UserTable).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_tokens(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Token).offset(skip).limit(limit).all()


def get_token_by_id(db: Session, token_id: int):
    return db.query(models.Token).filter(models.Token.id == token_id).first()


def add_jwt_in_db(db: Session, token: schemas.TokenBase) -> models.Token:
    db_token = models.Token(
        access_token=token.access_token,
        exp=token.exp,
        sub=token.sub,
        user_id=token.user_id,
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

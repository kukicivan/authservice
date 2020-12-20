import os
from enum import Enum
from typing import Tuple

import jwt
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from authservice import crud
from authservice.security.exceptions import InvalidCredentialsException
from authservice.login_manager import manager
from authservice.schemas import TokenBase

SECRET = os.getenv("SECRET")
pwd_context = CryptContext(schemes=["bcrypt"])


class JWTEnum(str, Enum):
    bearer = "Bearer <secret_token>"


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def verify_and_update_password(
        plain_password: str, hashed_password: str
) -> Tuple[bool, str]:
    return pwd_context.verify_and_update(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticator(db: Session, form_data: OAuth2PasswordRequestForm):
    user = crud.get_user_by_email(db, form_data.username)

    if user is None or not user.is_active:
        raise InvalidCredentialsException

    verified, updated_password_hash = verify_and_update_password(
        form_data.password, user.hashed_password
    )

    if not verified:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=form_data.username)
    )

    # decode token to get user_identifier (sub)
    payload = jwt.decode(access_token, SECRET)

    token: TokenBase = TokenBase(
        access_token=access_token,
        exp=payload.get("exp"),
        sub=payload.get("sub"),
        user_id=str(user.id) if user.id else str(99)
    )

    # save token in the database
    crud.add_jwt_in_db(db, token)

    return {'access_token': access_token, 'token_type': 'bearer'}

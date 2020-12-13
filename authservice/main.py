import uuid
from typing import Optional

import databases
import sqlalchemy
from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import FastAPIUsers, models
from fastapi_users.authentication import JWTAuthentication, BaseAuthentication, Authenticator
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi_users.db.sqlalchemy import GUID
from fastapi_users.router import ErrorCode
from sqlalchemy import Sequence, Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base, declared_attr
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

DATABASE_URL = "sqlite:///./test.db"
SECRET = "SECRET"


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


# TODO: Add table that will hold database token
from pydantic import UUID4, BaseModel, EmailStr, validator


class BaseToken(BaseModel):
    """Base SQLAlchemy users table definition."""

    # __tablename__ = "token"

    """Base User model."""

    id: Optional[UUID4] = None
    email: Optional[EmailStr] = None
    access_token: str
    expires_at: int
    refresh_token: Optional[str] = None

    is_superuser: Optional[bool] = False

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()

    # id = Column(GUID, primary_key=True)

    # Token
    # access_token = Column(String(length=1024), nullable=False)
    # expires_at = Column(Integer, nullable=False)
    # refresh_token = Column(String(length=1024), nullable=True)

    # Token properties
    # blacklisted = Column(Boolean, default=False, nullable=True)
    # created_at = Column(String(length=1024), nullable=True)
    # updated_at = Column(String(length=1024), nullable=True)
    # created_by = Column(GUID)
    # updated_by = Column(GUID)

    # Token data and user info
    # token_data: Column(String(length=1024), nullable=True)
    # user_email: Column(String(length=1024), nullable=True)
    # is_superuser = Column(Boolean, default=False)

    # TODO: Add ForeignKey on user.id attribute (with cascade delete)
    # @declared_attr
    # def user_id(cls):
    #     return Column(GUID, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class Token(BaseToken):
    pass


database = databases.Database(DATABASE_URL)
Base: DeclarativeMeta = declarative_base()


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


# class TokenTable(Base, Token):
#     pass


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
Base.metadata.create_all(engine)

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)


def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/login"
)

app = FastAPI()
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(
        SECRET, after_forgot_password=on_after_forgot_password
    ),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# router = APIRouter()
# backend = BaseAuthentication("base", True)
# authenticator = Authenticator(backend, user_db)


# def get_login_response(user, response):
#     return user
#
#
# @app.post("/login")
# async def login(
#         response: Response, credentials: OAuth2PasswordRequestForm = Depends()
# ):
#     user = await user_db.authenticate(credentials)
#
#     if user is None or not user.is_active:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
#         )
#
#     print("Hello world from override login method with DB support!")
#
#     return await backend.get_login_response(user, response)

# if backend.logout:
#     @router.post("/logout")
#     async def logout(
#             response: Response, user=Depends(authenticator.get_current_active_user)
#     ):
#         return await backend.get_logout_response(user, response)

# TODO: Override login to save token in Database
# TODO: Test how token is checked on each request
# TODO: Verify token against database token
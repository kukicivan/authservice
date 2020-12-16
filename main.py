import os
from urllib.request import Request

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from authservice import models, routes
from authservice.database import database, engine


class UserTable(models.Base, SQLAlchemyBaseUserTable):
    pass


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(models.UserDB, database, users)

# Create all table in database
models.Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI(
    title="Authentication service",
    description="This is a very fancy Authentication project built in Fast API. It have auto docs for the API and "
                "everything",
    version="0.0.1",
    docs_url="/",
    redoc_url="/redoc"
)


# After register hook
def on_after_register(user: models.UserDB, request: Request):
    print(f"User {user.id} has registered.")


# After forgot password hook
def on_after_forgot_password(user: models.UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")
    return token


SECRET = os.getenv("SECRET")
jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/login"
)

# Create Fast API users
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    models.User,
    models.UserCreate,
    models.UserUpdate,
    models.UserDB,
)

# Login route
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth", tags=["auth"]
)

# Register route
app.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

# Users routes
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

# Admin routes
app.include_router(routes.router)
app.include_router(
    routes.admin,
    dependencies=[Depends(routes.get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


print("INFO:     Auth service started")

# Used for debugger only
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Run uvicorn server for debugger.")

# TODO: Override login to save token in Database
# TODO: Test how token is verified on each request
# TODO: Verify token against database token


# router = APIRouter()
# backend = BaseAuthentication("base", True)
# authenticator = Authenticator(backend, user_db)


# def get_login_response(user, response):
#     return user


# @app.post("/auth/login")
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


# @app.post("/auth/login")
# def login(response: Response, data: OAuth2PasswordRequestForm = Depends()):
#     user_identifier = data.username
#     password = data.password
#
#     user = load_user(user_identifier)
#     if not user:
#         raise InvalidCredentialsException
#     elif password != user['password']:
#         raise InvalidCredentialsException
#
#     # access_token = manager.create_access_token(
#     #     data=dict(sub=user_identifier)
#     # )
#
#     access_token = "TOKEN-123"
#
#     return {'access_token': access_token, 'token_type': 'bearer'}

# def authenticator(args):
#     pass


# def get_current_active_user(args):
#     pass

# @app.post("/logout")
# async def logout(
#         response: Response, user=Depends(get_current_active_user)
# ):
#     return await backend.get_logout_response(user, response)

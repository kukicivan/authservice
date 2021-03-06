import os
from urllib.request import Request

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase

from authservice import models
from authservice import routes
from authservice.models import migrate, UserTable, UserDB

from core.middleware import add_middleware
from core.database import SqlAlchemyEngine, database

# Initialize Fast API framework
app: FastAPI = FastAPI(
    title="Authentication service",
    description="This is a very fancy Authentication project built in Fast API. "
                "It have auto docs for the API and everything",
    version="0.0.1",
    docs_url="/",
    redoc_url="/redoc"
)

# Add CORS middleware
add_middleware(app)


# Add after register hook
def on_after_register(user: models.UserDB, request: Request):
    print(f"User {user.id} has registered.")


# Add after forgot password hook
def on_after_forgot_password(user: models.UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")
    return token


# Initialize Fast API users with JWT backend
users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

# Create DB
migrate(SqlAlchemyEngine)

# Create auth backend
jwt_auth_backend = JWTAuthentication(secret=os.getenv("SECRET"), lifetime_seconds=3600, tokenUrl="/auth/login")

# Initialize auth service
auth_service = FastAPIUsers(
    user_db,
    [jwt_auth_backend],
    models.User,
    models.UserCreate,
    models.UserUpdate,
    models.UserDB,
)

# Add Login route
app.include_router(
    auth_service.get_auth_router(jwt_auth_backend), prefix="/auth", tags=["auth"]
)

# Add Register route
app.include_router(
    auth_service.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

# Add Users routes
app.include_router(auth_service.get_users_router(), prefix="/users", tags=["users"])

# Add Users list route
app.include_router(routes.users_router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

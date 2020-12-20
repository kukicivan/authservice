import os
from urllib.request import Request

import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from authservice import models, routes
from authservice.database import engine

from authservice.middleware import add_middleware
from authservice.models import migrate

# Create DB
user_db = migrate(engine)

# Create JWT Authentication Backend
SECRET = os.getenv("SECRET")
jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/login"
)

# Initialize Fast API
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


# Create Fast API Users
auth_service = FastAPIUsers(
    user_db,
    [jwt_authentication],
    models.User,
    models.UserCreate,
    models.UserUpdate,
    models.UserDB,
)

# Add Login route
# app.include_router(
#     auth_service.get_auth_router(jwt_authentication), prefix="/auth", tags=["auth"]
# )

# Add Register route
app.include_router(
    auth_service.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

# Add Users routes
app.include_router(auth_service.get_users_router(), prefix="/users", tags=["users"])

# Add Admin routes
app.include_router(routes.router)
app.include_router(routes.users_router)
app.include_router(routes.admin)

# App started
print("INFO:     Auth service started")

# Used for debugger only
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Run uvicorn server for debugger.")

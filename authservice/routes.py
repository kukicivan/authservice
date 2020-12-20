from fastapi import APIRouter, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from authservice import crud
from authservice.database import get_db

from authservice.security.service import authenticator
from authservice.schemas import User, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix="",
    tags=["auth"],
)

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

admin = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


@users_router.get("/", response_model=List[User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> List[User]:
    """
           Read all users with all the information:

           - **skip**: Number of records to be skipped
           - **limit**: Limit number of records that are returned from the request
           """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@admin.get("/token", response_model=List[Token], dependencies=[Depends(oauth2_scheme)])
def read_tokens(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
):
    """
           Read all tokens with all the information:

           - **skip**: Number of records to be skipped
           - **limit**: Limit number of records that are returned from the request
           """
    tokens = crud.get_tokens(db, skip=skip, limit=limit)
    return tokens


@admin.get("/token/{id}", response_model=Token or "null", dependencies=[Depends(oauth2_scheme)])
def read_token(
        id: int = Path(..., title="The ID of the token to get"),
        db: Session = Depends(get_db),
):
    """
           Read an token with all the information:

           - **id**: ID of the token
           """
    token = crud.get_tokens_by_id(db, id)

    if token:
        return token

    return token


# Override login to save token in the database
# TODO: Test how token is verified on each request
# TODO: Verify token against database token
@router.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return authenticator(db, form_data)

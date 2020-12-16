from enum import Enum

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from typing import List

from authservice import schemas, crud
from authservice.database import get_db

from fastapi import Header, HTTPException


class JWTEnum(str, Enum):
    bearer = "Bearer <secret_token>"


# TODO:
#  compere only first part of string,
#  to ensure that Bearer (with space after)
#  is presented in request header
async def get_token_header(request_jwt_token: JWTEnum = Header(...)):
    print(request_jwt_token)
    # Only Super User is able to list all tokens / sessions
    if request_jwt_token != JWTEnum.bearer:
        raise HTTPException(status_code=400, detail="Token header invalid. "
                                                    "Please provide "
                                                    "Authorization: Bearer <secret_token>.")


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Endpoint URL not found"}},
)

admin = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@router.get("/token", response_model=List[schemas.Token])
def read_tokens(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
           Read all tokens with all the information:

           - **skip**: Number of records to be skipped
           - **limit**: Limit number of records that are returned from the request
           """
    tokens = crud.get_tokens(db, skip=skip, limit=limit)
    return tokens


@admin.get("/token/{id}", response_model=schemas.Token or "null")
async def read_tokens(
        id: int = Path(..., title="The ID of the token to get"),
        db: Session = Depends(get_db)
):
    """
           Read an token with all the information:

           - **id**: ID of the token
           """

    # Get token from DB
    token = crud.get_tokens_by_id(db, id)

    if token:
        return token

    return token


@router.get("/allusers", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
           Read all users with all the information:

           - **skip**: Number of records to be skipped
           - **limit**: Limit number of records that are returned from the request
           """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

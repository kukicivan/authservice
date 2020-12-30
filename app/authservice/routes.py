from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List

from authservice.crud import get_users
from authservice.database import get_db
from authservice.schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.get("/", response_model=List[User])
async def read_users(
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
    users = await get_users(db, skip=skip, limit=limit)
    return users
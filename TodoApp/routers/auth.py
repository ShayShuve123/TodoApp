from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext

from dependencies import get_db
from db_modules import Users
from schemas.users import CreateUserRequest

auth_router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@auth_router.get("/", status_code=status.HTTP_200_OK)
def get_all_users(db: db_dependency):
    all_users = db.query(Users).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, )
    return all_users


@auth_router.post("/auth", status_code=status.HTTP_201_CREATED)
def create_user(create_user_requests: CreateUserRequest, db: db_dependency):
    """Create a new user"""
    create_user_module = Users(email=create_user_requests.email, username=create_user_requests.username,
                               first_name=create_user_requests.first_name, last_name=create_user_requests.last_name,
                               hashed_password=bcrypt_context.hash(create_user_requests.password), roles=create_user_requests.roles,
                               is_active=True)
    if create_user_requests:
        db.add(create_user_module)
        db.commit()
        db.refresh(create_user_module)

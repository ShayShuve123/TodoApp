from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from dependencies import get_db
from modules import Users
from schemas.users import CreateUserRequest

auth_router = APIRouter()
db_dependency = Depends(get_db)

@auth_router.get("/users", status_code=status.HTTP_200_OK)
def get_all_users(db: Session = db_dependency):
    all_users = db.query(Users).all()
    if not all_users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    return all_users

@auth_router.post("/auth", status_code=status.HTTP_201_CREATED)
def create_user(creat_user_requests: CreateUserRequest,db: Session = db_dependency ):
    """Create a new user"""
    create_user_module = Users(email = creat_user_requests.email,username = creat_user_requests.username ,
                first_name = creat_user_requests.first_name, last_name = creat_user_requests.last_name,
                hashed_password = creat_user_requests.password, roles = creat_user_requests.roles, is_active = True)
    if creat_user_requests:
        db.add(create_user_module)
        db.commit()
        db.refresh(create_user_module)
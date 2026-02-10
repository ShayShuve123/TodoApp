from fastapi import FastAPI

import db_modules
from routers import todos
from database import engine

from routers import auth

app = FastAPI()

db_modules.Base.metadata.create_all(bind=engine)  # rand only if the todos db will not exist

app.include_router(auth.auth_router, prefix="/users", tags=["auth"])
app.include_router(todos.todos_router, prefix="/todos", tags=["todos"])
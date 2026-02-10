from http import HTTPStatus
from typing import Annotated

from fastapi import Depends, HTTPException, Path, Body
from sqlalchemy.orm.session import Session

from fastapi import APIRouter

from dependencies import get_db
from modules import Todos

from schemas.todos import TodoRequest

todos_router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@todos_router.get("/")
def read_all_todos(db: db_dependency):  # TODO: fix--> up to python 3.9 Annotated[Session, Depends(get_db)
    return db.query(Todos).all()


@todos_router.get("/{todo_id}", status_code=HTTPStatus.OK)
def read_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    """Return a todo by id"""
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo:
        return todo
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Todo not found")


@todos_router.post("/create-todo", status_code=HTTPStatus.CREATED)
def create_todo(db: db_dependency, todo: TodoRequest = Body()):
    """Create a todo and save to DB"""
    new_todo = Todos(**todo.model_dump())
    try:
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
    except Exception:
        raise HTTPException(status_code=500, detail=f"Todo creation failed")


@todos_router.put("/update-todo/{todo_id}", status_code=HTTPStatus.OK)
def update_todo(db: db_dependency ,todo_id: int = Path(gt=0), todo: TodoRequest = Body()):
    """Update a todo and save to DB"""
    new_todo = Todos(**todo.model_dump())
    todo_module = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_module is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    try:
        todo_module.title = new_todo.title
        todo_module.complete = new_todo.complete
        todo_module.priority = new_todo.priority
        todo_module.description = new_todo.description

        db.commit()
        db.refresh(todo_module)

    except Exception:
        raise HTTPException(status_code=500, detail="Failed to update todo")


@todos_router.delete("/delete-todo/{todo_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    """Delete a todo and save to DB"""

    todo = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()


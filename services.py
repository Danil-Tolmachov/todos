from sqlalchemy.orm import Session
from database import SessionLocal
from routers.utils import hash_password

import models
import forms



# Get
async def get_user_by_id(db: Session, id: int) -> models.User:
    return db.query(models.User).get(id)


async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.username == username).first()


async def get_user_password(db: Session, id):
    return db.query(models.User).get(id).hashed_password


async def get_user_todos(db: Session, id: int = None, username: str = None) -> list[models.Todo]:
    pass


async def get_user_todo(db: Session, id: int = None, username: str = None) -> models.Todo:
    pass



# Create
async def create_user(db: Session, user: forms.UserForm) -> models.User:
    pass


async def create_todo(db: Session, todo: forms.TodoForm) -> models.Todo:
    pass



# Update
async def update_user(db: Session, user: forms.UserForm) -> models.User:
    pass


async def update_todo(db: Session, todo: forms.TodoForm) -> models.Todo:
    pass



# Delete
async def delete_user(db: Session, id: int) -> None:
    pass


async def delete_todo(db: Session, id: int) -> None:
    pass

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


async def get_user_todos(db: Session, id: int = None) -> list[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.user_id == id)
    

async def get_todo(db: Session, id: int) -> models.Todo:
    return db.query(models.Todo).filter(models.Todo.id == id).first()



# Create
async def create_user(db: Session, user: forms.UserForm) -> models.User:
    """
    Creates a new user in the database with the provided user details.

    Args:
    - db (Session): the database session object to execute the query.
    - user (forms.UserForm): the UserForm instance containing user details.

    Returns:
    - models.User: the User model object created in the database.
    - None: returns None if a user with the same username already exists in the database.

    Raises:
    - SQLAlchemyError: If there was an error while accessing the database.
    """

    if await get_user_by_username(db, user.username) is not None:
        return None

    user_model = models.User()

    user_model.username = user.username
    user_model.hashed_password = hash_password(user.password)
    user_model.email = user.email

    db.add(user_model)
    db.commit()

    return user_model


async def create_todo(db: Session, todo: forms.TodoForm, user_id: int) -> models.Todo or None:
    """
    Create a new todo item in the database.

    Args:
        - db (Session): SQLAlchemy database session.
        - todo (forms.TodoForm): A dataclass representing the todo item to be created.

    Returns:
        - models.Todo or None: The created todo item if successful, otherwise None.
    """

    if not await get_user_by_id(user_id):
        return None

    todo_model = models.Todo()

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.importance = todo.importance
    todo_model.complete = False
    todo_model.user_id = user_id

    db.add(todo_model)
    db.commit()

    return todo_model



# Update
async def update_user(db: Session, user: forms.UserForm) -> models.User:
    """
    Update an existing user with the given user form data.

    Args:
        db (Session): The database session object.
        user (forms.UserForm): The user form data to update the user with.

    Returns:
        models.User: The updated user model.
    """
    user_model = await get_user_by_id(db, user.id)

    user_model.username = user.username
    user_model.email = user.email
    user_model.hashed_password = hash_password(user.password)

    db.add(user_model)
    db.commit()
    return user_model


async def update_todo(db: Session, todo: forms.TodoForm) -> models.Todo:
    """
    Updates an existing todo item in the database.

    Args:
    - db (Session): database session object.
    - todo (forms.TodoForm): a TodoForm instance with the new data to update the todo item.

    Returns:
    - models.Todo: the updated Todo model instance.
    """
    todo_model = await get_todo(db, todo.id)

    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.importance = todo.importance

    db.add(todo_model)
    db.commit()
    return todo_model


async def change_todo_complete(db: Session, id: int):
    """
    Toggles the completion status of a todo item in the database.

    Args:
    - db (Session): database session object.
    - id (int): ID of the todo item to update.

    Returns:
    - models.Todo: the updated todo item model.
    """
    todo = await get_todo(db, id)

    if todo.complete == False:
        todo.complete = True
    else:
        todo.complete = False

    db.add(todo)
    db.commit()
    return todo



# Delete
async def delete_user(db: Session, id: int) -> bool:
    """
    Toggles the completion status of a todo item in the database.

    Args:
    - db (Session): database session object.
    - id (int): ID of the todo item to update.

    Returns:
    - models.Todo: the updated todo item.
    """
    user = await get_user_by_id(db, id)

    if user is None:
        return False
    
    user.delete()
    db.commit()
    return True


async def delete_todo(db: Session, todo_id: int) -> bool:
    """
    Deletes a todo item with the given ID.

    Args:
    - db (Session): database session object.
    - id (int): the ID of the todo item to be deleted.

    Returns:
    - bool: True if the todo item was deleted successfully, False if the item was not found.
    """
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id)

    if todo is None:
        return False
    
    todo.delete()
    db.commit()
    return True

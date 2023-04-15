from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from config import templates
from sqlalchemy.orm import Session
from database.setup import get_db
from utils.exceptions import get_404
from routers.auth import token_required
from database.models import User

from database import services
from utils import forms


router = APIRouter()



@router.get('/', name='index')
async def index_page(request: Request, 
                     user: User = Depends(token_required), 
                     db: Session = Depends(get_db)):
    
    todos = await services.get_user_todos(db, user.id)

    context = {
        'request': request,
        'user': user,
        'todos': todos,
    }

    return templates.TemplateResponse('home.html', context)



@router.get('/add-todo', name='add-todo')
async def create_todo_page(request: Request, user: User = Depends(token_required)):
    return templates.TemplateResponse('add-todo.html', {'request': request})

@router.post('/add-todo')
async def create_todo(title = Form(),
                      description= Form(),
                      priority = Form(),
                      db: Session = Depends(get_db),
                      user: User = Depends(token_required)):
    
    todo = forms.TodoForm(title=title, description=description, importance=priority)
    
    await services.create_todo(db, todo, user.id)

    return RedirectResponse('/todos', status_code=status.HTTP_302_FOUND)



@router.get('/complete/{todo_id}')
async def complete_todo(todo_id: int, 
                        user: User = Depends(token_required),
                        db: Session = Depends(get_db)):
    
    if (await services.get_todo(db, todo_id)).user_id != user.id:
        raise get_404()

    await services.change_todo_complete(db, todo_id)

    return RedirectResponse('/todos', status_code=status.HTTP_302_FOUND)


@router.get('/edit-todo/{todo_id}', name='edit-todo')
async def update_todo_page(request: Request, todo_id: int, 
                           user: User = Depends(token_required), 
                           db: Session = Depends(get_db)):

    todo = await services.get_todo(db, id=todo_id)

    if todo is None:
        raise get_404()

    if todo.user_id != user.id:
        return RedirectResponse('todos/', status_code=status.HTTP_403_FORBIDDEN)

    context = {
        'request': request,
        'todo': todo
    }

    return templates.TemplateResponse('edit-todo.html', context)


@router.post('/edit-todo/{todo_id}', name='edit-todo')
async def update_todo(todo_id: int,
                      title = Form(),
                      description = Form(),
                      priority = Form(),
                      user: User = Depends(token_required),
                      db: Session = Depends(get_db)):
    
    if (await services.get_todo(db, todo_id)).user_id != user.id:
        raise get_404()
    
    todo = forms.TodoForm(id=todo_id, title=title, 
                          description=description,
                          importance=priority)
    
    await services.update_todo(db, todo)
    return RedirectResponse('/todos', status_code=status.HTTP_302_FOUND)


@router.get('/delete/{todo_id}')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):

    if not await services.get_todo(db, todo_id):
        raise get_404()

    await services.delete_todo(db, todo_id)
    return RedirectResponse('/todos', status_code=status.HTTP_302_FOUND)

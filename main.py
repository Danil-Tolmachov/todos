from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from starlette import status
from starlette.staticfiles import StaticFiles
from database.setup import engine

from routers import auth, todos
from config import templates
from database.models import Base

import uvicorn



Base.metadata.create_all(bind=engine)



app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(
    auth.router,
    prefix='/auth',
    tags=['auth'],
    responses={401:{'User': 'Not authorized'}}
)

app.include_router(
    todos.router,
    prefix='/todos',
    tags=['todos'],
)



@app.exception_handler(401)
async def not_authorized_handler(request, exc):
    return RedirectResponse('/auth/login')


@app.exception_handler(404)
async def get_404_template(request: Request, exc):
    return templates.TemplateResponse('http404.html', context={'request': request}, status_code=status.HTTP_404_NOT_FOUND)


# @app.exception_handler(405)
# async def method_not_allowed_handler(request, exc):
#     return RedirectResponse('/', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/')
async def redirect():
    return RedirectResponse('/todos', status_code=status.HTTP_308_PERMANENT_REDIRECT)



# Run app
if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

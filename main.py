from fastapi import FastAPI
from database import engine

from routers import auth, todos
from models import Base

import uvicorn


Base.metadata.create_all(bind=engine)



app = FastAPI()

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



# Test
@app.get('/')
async def test():
    return {'status': 'Successful'}


# Run app
if __name__ == '__main__':
    uvicorn.run(app)

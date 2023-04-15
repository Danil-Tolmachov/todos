from fastapi import APIRouter, Depends, Form, Cookie, Request, Response
from fastapi.responses import RedirectResponse
from starlette import status
from sqlalchemy.orm import Session

from utils.tokens import delete_access_token, verify_password, set_access_token, token_decode, token_encode, token_validation
from utils.exceptions import get_auth_exception, get_expired_token_exception, get_missing_token_exception, get_invalid_token_exception
from database.setup import get_db
from config import templates

from database import services
from utils import forms


router = APIRouter()



async def check_password(db: Session, id: int, password: str):
    """
    Checks if the password passed as an argument matches the hash of the password for the user with the specified ID.

    Args:
    - db (Session): database session object.
    - id (int): ID of the user to check the password for.
    - password (str): password to check.

    Returns:
    - bool: True if the password matches the hash of the user's password, False otherwise.
    """
    hash = await services.get_user_password(db, id)

    if verify_password(password, hash):
        return True
    
    return False


async def authenticate_user(db, username: str = None, password: str = None, token: str = None):
    """
    Authenticates the user based on the provided username and password or token.

    Args:
    - db (Session): database session object.
    - username (str): username of the user to authenticate.
    - password (str): password of the user to authenticate.
    - token (str): token of the user to authenticate.

    Returns:
    - dict: dictionary with user data if the user is authenticated, None otherwise.
    """

    user = None

    if token:
        data = token_decode(token)
        user_id = data.get('id')
        
        if user_id:
            user = await services.get_user_by_id(db, user_id)

    elif username and password:
            user = await services.get_user_by_username(db, username)

            if user is None:
                return None
            
            if not await check_password(db, user.id, password=password):
                return None

    return user



async def login_user(db, username, password, response: Response = None):
    """
    Authenticates a user using the given username and password.

    Args:
        db (Session): The database session object.
        username (str): The username of the user.
        password (str): The password of the user.
        response (Response, optional): The response object. Defaults to None.

    Returns:
        Response: The response object.
    """
    user = await authenticate_user(db, username=username, password=password)
    
    if response is None:
        response = RedirectResponse('/todos', status_code=status.HTTP_302_FOUND)

    if user is None:
        raise get_auth_exception()
    
    set_access_token(response, token_encode(user.id, user.username))
    return response


async def logout_user(db, response: Response = None):
    """
    Log out a user by deleting their access token.

    Args:
        db (Session): A database session dependency.
        response (Response): Optional response object. If provided, the access token will be deleted from the cookie in this response.

    Returns:
        Response object
    """
    if response is None:
        response = RedirectResponse('/auth/login', status_code=status.HTTP_302_FOUND)

    delete_access_token(response)
    return response



async def token_required(db: Session = Depends(get_db), access_token = Cookie(default=None)):
    """
    Decorator function that requires an access token to access the protected endpoints.

    Args:
    - db (Session): database session object.
    - access_token (str): access token passed as a cookie.

    Returns:
    - dict: dictionary with user data if the token is valid, otherwise an exception is raised.
    """

    if access_token is None:
        raise get_missing_token_exception()
    
    if not token_validation(access_token):
        raise get_expired_token_exception()
    
    user = await authenticate_user(db, token=access_token)
    
    if user is None:
        raise get_invalid_token_exception()
    
    return user




# Login Page
@router.get('/login')
async def login_page(request: Request):

    context = {
        'request': request,
    }

    return templates.TemplateResponse('login.html', context)

# Login Endpoint
@router.post('/login-user')
async def login_page(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    response = await login_user(db, username, password)
    return response

# Logout Page
@router.get('/logout')
async def logout_page(db: Session = Depends(get_db)):
    return await logout_user(db)


# Register Page
@router.get('/register', name='register')
async def register_page(request: Request):

    context = {
        'request': request,
    }

    return templates.TemplateResponse('register.html', context)


# Register Endpoint
@router.post('/create-user')
async def create_user(db: Session = Depends(get_db),
                   username = Form(), email = Form(),
                   password = Form(), password2 = Form(),
                   ):
    
    user = forms.UserForm(username=username, email=email,
                          password=password, password2=password2)

    user = await services.create_user(db, user)

    if user is None:
        return RedirectResponse('/auth/register', status_code=status.HTTP_303_SEE_OTHER)

    return await login_user(db, username, password)


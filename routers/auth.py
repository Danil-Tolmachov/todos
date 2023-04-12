from fastapi import APIRouter, Depends, Form, Cookie, Response
from sqlalchemy.orm import Session

from routers.utils import verify_password, set_access_token, token_decode, token_encode, token_validation
from exceptions import get_auth_exception, get_expired_token_exception, get_missing_token_exception, get_invalid_token_exception
from database import get_db

import services



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



# @router.get('/get-token')
# async def get_token():
#     token = await token_encode(1, 'daniltol')
#     return {'token': token}
# 
# @router.get('/token-check/{token}')
# async def get_token(token: str = Path()):
#     is_active = await token_expiration_check(token)
#     return {'is_active': is_active}
# 
# @router.get('/token-user/{token}')
# async def get_user(token: str = Path(), db: Session = Depends(get_db)):
#     user = await authenticate_user(db, token=token)
#     return {'user': user}


@router.post('/login-user')
async def password_login_endpoint(username: str = Form(), password: str = Form(), db: Session = Depends(get_db)):
    user = await authenticate_user(db, username=username, password=password)
    
    if user is None:
        raise get_auth_exception()
    
    response = Response(status_code=200)
    set_access_token(response, token_encode(user.id, user.username))

    return response


@router.get('/my-user')
async def get_user(user = Depends(token_required), db: Session = Depends(get_db)):
    return user


@router.get('/test')
async def test_authorization(user = Depends(token_required), db: Session = Depends(get_db)):
    return {'Authorization': 'Successful'}

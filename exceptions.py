from fastapi.exceptions import HTTPException
from config import templates

from starlette import status



def get_auth_exception():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authorized')


def get_missing_token_exception():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')


def get_invalid_token_exception():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')


def get_expired_token_exception():
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token has expired')


def get_invalid_data_exception():
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid data')


def get_404():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

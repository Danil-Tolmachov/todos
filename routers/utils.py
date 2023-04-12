from datetime import datetime, timedelta
from typing import Optional
from fastapi import Response
from jose import jwt, JWTError
from fastapi.encoders import jsonable_encoder

import models
import config



def token_encode(id: int, username: str, expire_delta: Optional[timedelta] = None):
    """
    Encodes a JWT token with the provided user ID, username and expiration time.

    Args:
    - id (int): user ID.
    - username (str): username of the user.
    - expire_delta (Optional[timedelta]): optional expiration time of the token in minutes.

    Returns:
    - str: encoded JWT token.
    """

    # Expire date setup
    if expire_delta is None:
        expire_date = datetime.utcnow() + timedelta(minutes=30)
    else:
        expire_date = datetime.utcnow() + expire_delta

    # Payload setup
    payload = {
        'id': id,
        'username': username,
        'expire': jsonable_encoder(expire_date),
    }
    
    return jwt.encode(payload, config.SECRET_KEY, config.ALGORITHM)



def token_decode(token: str) -> dict:
    """
    Decodes a JWT token and returns a dictionary with its payload.

    Args:
    - token (str): The JWT token to be decoded.

    Returns:
    - dict: A dictionary containing the payload of the JWT token.

    Raises:
    - jwt.exceptions.InvalidTokenError: If the token is invalid or cannot be decoded.
    """
    return jwt.decode(token, config.SECRET_KEY, config.ALGORITHM)



def set_access_token(response: Response, token):
    """
    Sets the access token as a cookie in the provided response object.

    Args:
    - response (fastapi.Response): the response object to set the cookie in.
    - token (str): the access token to set as a cookie.
    """
    response.set_cookie(key='access_token', value=token)
    


def token_validation(token) -> bool:
    """
    Validates whether a token has expired or not.

    Args:
    - token (str): the token to validate.

    Returns:
    - bool: True if the token is valid, False if it has expired.
    """

    expiration_date: str = token_decode(token).get('expire')

    # Return True if token doesn't expire
    if datetime.utcnow() > datetime.fromisoformat(expiration_date):
        return False
    
    return True



def hash_password(password: str):
    """
    Hashes a password using bcrypt.

    Args:
    - password (str): the password to hash.

    Returns:
    - str: the hashed password.
    """
    return config.bcrypt_context.hash(password)


def verify_password(password: str, hash: str) -> bool:
    """
    Verifies if a password matches a hash using bcrypt.

    Args:
    - password (str): the password to verify.
    - hash (str): the hashed password to compare against.

    Returns:
    - bool: True if the password matches the hash, False otherwise.
    """
    return config.bcrypt_context.verify(password, hash)

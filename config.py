from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv


# load environment from '.env' file
env = load_dotenv('.env')

# Encrypting vars
ALGORITHM = 'HS256'
SECRET_KEY = getenv('SECRET_KEY')
bcrypt_context = CryptContext(['bcrypt'], deprecated='auto')

# Use "True" only for development
DEBUG = getenv('DEBUG', False)

# Database settings
DATABASE_URL = getenv('DATABASE_URL')
DATABASE_USER = getenv('DATABASE_USER')
DATABASE_PASSWORD = getenv('DATABASE_PASSWORD')

# Templating settings
templates = Jinja2Templates('templates')

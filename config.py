from functools import lru_cache
from dotenv import load_dotenv
from os import getenv


# load environment from '.env' file
env = load_dotenv('.env')


# Use "True" only for development
DEBUG = getenv('DEBUG', False)

DATABASE_URL = getenv('DATABASE_URL')
DATABASE_USER = getenv('DATABASE_USER')
DATABASE_PASSWORD = getenv('DATABASE_PASSWORD')

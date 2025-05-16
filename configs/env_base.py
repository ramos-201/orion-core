import os


ENDPOINT_NAME = '/graphql'

DB_NAME = os.environ['DB_NAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
DB_URL = os.environ['DB_URL']
DB_USER = os.environ['DB_USER']

SECRET_KEY_TOKEN = os.environ['SECRET_KEY_TOKEN']
ALGORITHM_TOKEN = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES_TOKEN = os.environ['ACCESS_TOKEN_EXPIRE_MINUTES_TOKEN']

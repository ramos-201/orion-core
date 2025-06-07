import os


# Database Postgres
DB_NAME = os.environ['DB_NAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
DB_URL = os.environ['DB_URL']
DB_USER = os.environ['DB_USER']

# JWT token
PRIVATE_KEY_JWT = os.environ['PRIVATE_KEY_JWT']
ALGORITHM_JWT = 'HS256'
MINUTES_EXPIRATION_JWT = os.environ['MINUTES_EXPIRATION_JWT']

import os


# Database Postgres
DB_NAME = os.environ['DB_NAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
DB_URL = os.environ['DB_URL']
DB_USER = os.environ['DB_USER']


# Database Postgres Test
TEST_DB_NAME = 'db_orion_test'
TEST_DB_PASSWORD = 'password_orion_test'
TEST_DB_PORT = 5435
TEST_DB_URL = 'localhost'
TEST_DB_USER = 'user_orion_test'


# JWT token
PRIVATE_KEY_JWT = os.environ['PRIVATE_KEY_JWT']
ALGORITHM_JWT = 'HS256'
MINUTES_EXPIRATION_JWT = os.environ['MINUTES_EXPIRATION_JWT']

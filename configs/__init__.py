import os

from dotenv import load_dotenv


if not os.getenv('LOADED_ENV'):
    load_dotenv('.env')
    os.environ['LOADED_ENV'] = '1'

ENV = os.getenv('ENVIRONMENT', '').lower()

if ENV == 'dev':
    from .env_dev import *  # noqa: F401, F403
elif ENV == 'main':
    from .env_main import *  # noqa: F401, F403
else:
    if ENV:
        raise ValueError(f' The environment `{ENV}` is not set up.')
    else:
        raise ValueError(' The `.env` file was not found. Define the `ENVIRONMENT` variable correctly.')

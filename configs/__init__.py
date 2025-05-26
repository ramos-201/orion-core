import logging
import os
import sys

from dotenv import load_dotenv


logger = logging.getLogger(' UPLOAD_ENV')
logging.basicConfig(level=logging.INFO)


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
        logger.error(f' The environment `{ENV}` is not set up.')
    else:
        logger.error(' The `.env` file was not found. Define the `ENVIRONMENT` variable correctly.')
    sys.exit(1)

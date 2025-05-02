import re

from ariadne import graphql
from graphql import GraphQLError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from tortoise import Tortoise

from configs import (
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_URL,
    DB_USER,
    IS_DEV,
)
from src.api.schemas import schema
from src.constants import (
    ENDPOINT_NAME,
    ErrorTypeEnum,
)


async def graphql_endpoint(request: Request):
    data = await request.json()
    query = data.get('query')
    variables = data.get('variables')

    payload = {'query': query, 'variables': variables}
    _, result = await graphql(
        schema,
        payload,
        context_value={'request': request},
        error_formatter=error_formatter,
    )

    return JSONResponse(result)


def error_formatter(error: GraphQLError, _) -> dict:
    message = 'An unknown error occurred'
    error_type = ErrorTypeEnum.UNKNOWN_ERROR

    if isinstance(error, GraphQLError):
        raw_message = str(error.message)
        message = re.sub(r"[\"']", '', raw_message)
        error_type = error.extensions.get('error_type', ErrorTypeEnum.INTERNAL_ERROR.value)

    return {
        'error_type': error_type,
        'message': message,
    }


async def init_db():
    await Tortoise.init(
        db_url=f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}',
        modules={'models': ['src.models']},
    )
    if IS_DEV:
        await Tortoise.generate_schemas()


async def close_db():
    await Tortoise.close_connections()


routes = [
    Route(ENDPOINT_NAME, graphql_endpoint, methods=['POST']),
]


app = Starlette(routes=routes, on_startup=[init_db], on_shutdown=[close_db])

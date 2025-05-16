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
    ENDPOINT_NAME,
    IS_DEV,
)
from src.api.schemas import schema
from src.constants import ErrorTypeEnum
from src.utils.jwt_handler import decode_access_token


async def get_context(request: Request):
    context = {'request': request, 'user_id': None}
    header = request.headers.get('Authorization', '')

    if header.startswith('Bearer '):
        token = header.split(' ', 1)[1]
        context['user_id'] = decode_access_token(token=token)
    return context


async def graphql_endpoint(request: Request):
    data = await request.json()

    query = data.get('query')
    context = await get_context(request)
    variables = data.get('variables')
    payload = {'query': query, 'variables': variables}

    _, result = await graphql(
        schema,
        payload,
        context_value=context,
        error_formatter=error_formatter,
    )

    return JSONResponse(result)


def error_formatter(error: GraphQLError, _):
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

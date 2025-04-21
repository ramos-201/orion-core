import re

from ariadne import graphql_sync
from graphql import GraphQLError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.constants import (
    ENDPOINT_NAME,
    ErrorTypeEnum,
)
from src.api.schemas import schema


async def graphql_endpoint(request: Request):
    data = await request.json()
    query = data.get('query')
    variables = data.get('variables')

    _, result = graphql_sync(
        schema,
        {
            'query': query,
            'variables': variables,
        },
        context_value={'request': request},
        error_formatter=error_formatter,
    )

    return JSONResponse(result)


def error_formatter(error, debug):
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


routes = [
    Route(ENDPOINT_NAME, graphql_endpoint, methods=['POST']),
]

app = Starlette(routes=routes)

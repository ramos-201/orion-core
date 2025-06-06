from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.gql.execute_gql import (
    execute_app_gql,
    execute_user_gql,
)


USER_GQL_ENDPOINT = '/user'
APP_GQL_ENDPOINT = '/app'


async def _execute_gql(request: Request, executor) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    variables = data.get('variables')

    _, result = await executor(
        payload={'query': query, 'variables': variables},
        context={'request': request},
    )

    return JSONResponse(result)


async def _execute_user_gql(request: Request) -> JSONResponse:
    return await _execute_gql(request, execute_user_gql)


async def _execute_app_gql(request: Request) -> JSONResponse:
    return await _execute_gql(request, execute_app_gql)


router = [
    Route(USER_GQL_ENDPOINT, _execute_user_gql, methods=['POST']),
    Route(APP_GQL_ENDPOINT, _execute_app_gql, methods=['POST']),
]

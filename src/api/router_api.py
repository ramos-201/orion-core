from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.management.schema import execute_schema
from src.controllers.user_controller import UserController
from src.utils.jwt_handler import decode_access_token


GRAPHQL_ENDPOINT = '/graphql'


async def _get_context(request) -> dict[str, Any]:
    context = {
        'request': request,
        'user': None,
    }

    header = request.headers.get('Authorization', '')

    if header.startswith('Bearer '):
        token = header.split(' ', 1)[1]
        user_id = decode_access_token(token=token)

        if user_id:
            user_controller = UserController()
            user = await user_controller.get_user_by_id(user_id=user_id)

            context['user'] = user

    return context


async def _execute_graphql_endpoint(request: Request) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    variables = data.get('variables')

    payload = {
        'query': query,
        'variables': variables,
    }
    context = await _get_context(request)

    _, result = await execute_schema(graphql_payload=payload, context=context)

    return JSONResponse(result)


router = [
    Route(
        GRAPHQL_ENDPOINT,
        _execute_graphql_endpoint,
        methods=['POST'],
    ),
]

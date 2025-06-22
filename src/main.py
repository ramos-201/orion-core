from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.db_config import (
    close_db,
    initialize_db,
)
from src.gql.resolvers import execute_gql


AUTH_GQL_ENDPOINT = '/graphql-auth'


async def execute_auth_endpoint(request: Request) -> JSONResponse:
    data = await request.json()
    _, result = await execute_gql(data=data)
    return JSONResponse(result)


app = Starlette(
    routes=[
        Route(AUTH_GQL_ENDPOINT, execute_auth_endpoint, methods=['POST']),
    ],
    on_startup=[initialize_db],
    on_shutdown=[close_db],
)

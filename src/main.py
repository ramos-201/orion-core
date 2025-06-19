from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


AUTH_ENDPOINT = '/auth'


async def execute_auth_endpoint(request: Request) -> JSONResponse:
    return JSONResponse({'message': True})


app = Starlette(
    routes=[
        Route(AUTH_ENDPOINT, execute_auth_endpoint, methods=['POST']),
    ],
)

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route


ENDPOINT_NAME = '/graphql'


async def graphql_endpoint(request: 'Request') -> 'JSONResponse':
    return JSONResponse({'OK': True})


router = [
    Route(
        ENDPOINT_NAME,
        graphql_endpoint,
        methods=['POST'],
    ),
]

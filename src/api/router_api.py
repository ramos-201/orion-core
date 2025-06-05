from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.management.schema import execute_schema


GRAPHQL_ENDPOINT = '/graphql'


async def _execute_graphql_endpoint(request: Request) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    variables = data.get('variables')

    _, result = await execute_schema(
        graphql_payload={'query': query, 'variables': variables},
        context={'request': request},
    )

    return JSONResponse(result)


router = [
    Route(
        GRAPHQL_ENDPOINT,
        _execute_graphql_endpoint,
        methods=['POST'],
    ),
]

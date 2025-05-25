from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.management.execute_schema import execute_schema


GRAPHQL_ENDPOINT = '/graphql'


async def graphql_endpoint(request: Request) -> JSONResponse:
    data = await request.json()
    query = data.get('query')
    variables = data.get('variables')

    payload = {
        'query': query,
        'variables': variables,
    }
    context = {'request': request}

    _, result = await execute_schema(graphql_payload=payload, context=context)

    return JSONResponse(result)


routes = [
    Route(
        GRAPHQL_ENDPOINT,
        graphql_endpoint,
        methods=['POST'],
    ),
]

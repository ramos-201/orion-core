from ariadne import graphql_sync
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

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
    )

    return JSONResponse(result)


routes = [
    Route('/graphql', graphql_endpoint, methods=['POST']),
]

app = Starlette(routes=routes)

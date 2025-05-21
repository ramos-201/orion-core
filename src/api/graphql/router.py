from ariadne import graphql
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.graphql.schema import schema
from src.api.graphql.utils.get_context_gql import get_context
from src.api.graphql.utils.get_error_formatter_gql import get_error_formatter


ENDPOINT_NAME = '/graphql'


async def graphql_endpoint(request: Request) -> JSONResponse:
    data_request = await request.json()

    query = data_request.get('query')
    variables = data_request.get('variables')
    context = await get_context(request)

    _, result = await graphql(
        schema,
        {'query': query, 'variables': variables},
        context_value=context,
        error_formatter=get_error_formatter,
    )

    return JSONResponse(result)


router_gql = [
    Route(ENDPOINT_NAME, graphql_endpoint, methods=['POST']),
]

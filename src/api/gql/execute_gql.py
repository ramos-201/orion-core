from typing import Any

from ariadne import (
    graphql,
    make_executable_schema,
)
from ariadne.executable_schema import SchemaBindables
from ariadne.types import GraphQLResult

from src.api.gql.app.mutations.mutations import mutation as app_mutation
from src.api.gql.app.queries.query import query as app_query
from src.api.gql.app.typedef import typedefs as app_typedefs
from src.api.gql.user.mutations.mutation import mutation as user_mutation
from src.api.gql.user.queries.query import query as user_query
from src.api.gql.user.typedef import typedefs as user_typedefs
from src.api.gql.utils.error_formatter_gql import get_error_formatter_gql


async def _execute_gql_request(
    payload: dict[str, Any],
    context: dict[str, Any],
    typedefs: str,
    query: SchemaBindables,
    mutation: SchemaBindables,
) -> GraphQLResult:
    schema = make_executable_schema(
        typedefs,
        query,
        mutation,
        convert_names_case=True,
    )

    return await graphql(
        schema,
        payload,
        context_value=context,
        error_formatter=get_error_formatter_gql,
    )


async def execute_app_gql(payload: dict[str, Any], context: dict[str, Any]) -> GraphQLResult:
    return await _execute_gql_request(
        payload=payload,
        context=context,
        typedefs=app_typedefs,
        query=app_query,
        mutation=app_mutation,
    )


async def execute_user_gql(payload: dict[str, Any], context: dict[str, Any]) -> GraphQLResult:
    return await _execute_gql_request(
        payload=payload,
        context=context,
        typedefs=user_typedefs,
        query=user_query,
        mutation=user_mutation,
    )

from typing import Any

from ariadne import (
    graphql,
    make_executable_schema,
)
from ariadne.types import GraphQLResult

from src.api.management.graphql.mutations.mutation import mutation_gql
from src.api.management.graphql.queries import query_gql
from src.api.management.graphql.typedef import type_defs


async def execute_schema(graphql_payload: dict[str, Any], context: dict[str, Any]) -> GraphQLResult:
    schema = make_executable_schema(
        type_defs,
        query_gql,
        mutation_gql,
        convert_names_case=True,
    )
    return await graphql(schema, graphql_payload, context_value=context)

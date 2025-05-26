from typing import Any

from ariadne import (
    graphql,
    make_executable_schema,
)
from ariadne.types import GraphQLResult

from src.api.management.graphql.mutations.mutations import mutation
from src.api.management.graphql.queries import query
from src.api.management.graphql.typedef import type_defs


async def execute_schema(graphql_payload: dict[str, Any], context: dict[str, Any]) -> GraphQLResult:
    schema = make_executable_schema(
        type_defs,
        query,
        mutation,
        convert_names_case=True,
    )
    return await graphql(schema, graphql_payload, context_value=context)

import re
from typing import Any

from ariadne import (
    graphql,
    make_executable_schema,
)
from ariadne.types import GraphQLResult
from graphql import GraphQLError

from src.api.management.graphql.mutations.mutations import mutation
from src.api.management.graphql.queries.query import query
from src.api.management.graphql.typedef import type_defs
from src.utils.constants import ErrorTypeEnum


def _get_error_formatter(error: GraphQLError, _) -> dict:
    message_error = 'An unknown error occurred.'
    error_type = ErrorTypeEnum.UNKNOWN_ERROR.value

    if isinstance(error, GraphQLError):
        raw_message = str(error.message)
        message_error = re.sub(r"[\"']", '', raw_message)

        original_error = getattr(error, 'original_error', None)

        if original_error:
            error_type = getattr(original_error, 'error_type', error_type)
        else:
            error_type = error.extensions.get('error_type', ErrorTypeEnum.INTERNAL_ERROR.value)

    return {
        'error_type': error_type,
        'message': message_error,
    }


async def execute_schema(graphql_payload: dict[str, Any], context: dict[str, Any]) -> GraphQLResult:
    schema = make_executable_schema(
        type_defs,
        query,
        mutation,
        convert_names_case=True,
    )
    return await graphql(
        schema,
        graphql_payload,
        context_value=context,
        error_formatter=_get_error_formatter,
    )

import re

from ariadne import graphql
from graphql import GraphQLError

from src.enums.error_type_enum import ErrorTypeEnum
from src.gql.resolvers.auth.schema import schema


def _get_error_formatter_gql(error: GraphQLError, _) -> dict:
    message_error = 'An unknown error occurred.'
    error_type = ErrorTypeEnum.UNKNOWN_ERROR.value
    details = dict

    if isinstance(error, GraphQLError):
        raw_message = str(error.message)
        message_error = re.sub(r"'([^']*)'", r'"\1"', raw_message)

        original_error = getattr(error, 'original_error', None)

        if original_error:
            error_type = getattr(original_error, 'error_type', error_type)
            details = getattr(original_error, 'details', details)
        else:
            error_type = error.extensions.get('error_type', ErrorTypeEnum.INTERNAL_ERROR.value)

    return {
        'error_type': error_type,
        'message': message_error,
        'details': details,
    }


async def execute_gql(data):
    return await graphql(
        schema,
        data,
        context_value={},
        error_formatter=_get_error_formatter_gql,
    )

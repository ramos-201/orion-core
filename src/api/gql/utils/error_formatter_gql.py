import re
from typing import Any

from graphql import GraphQLError

from src.utils.constants import ErrorTypeEnum


def get_error_formatter_gql(error: GraphQLError, _) -> dict[str, Any]:
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

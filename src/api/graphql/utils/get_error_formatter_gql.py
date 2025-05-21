import re

from graphql import GraphQLError

from src.utils.constants import ErrorTypeEnum


def get_error_formatter(error: GraphQLError, _) -> dict:
    message_error = 'An unknown error occurred'
    error_type = ErrorTypeEnum.UNKNOWN_ERROR

    if isinstance(error, GraphQLError):
        raw_message = str(error.message)
        message_error = re.sub(r"[\"']", '', raw_message)
        error_type = error.extensions.get('error_type', ErrorTypeEnum.INTERNAL_ERROR.value)

    return {
        'error_type': error_type,
        'message': message_error,
    }

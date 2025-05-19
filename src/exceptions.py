from graphql import GraphQLError

from src.constants import ErrorTypeEnum


class MutationError(GraphQLError):
    def __init__(self, message: str, error_type: ErrorTypeEnum):
        super().__init__(message, extensions={'error_type': error_type.value})

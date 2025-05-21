from graphql import GraphQLError

from src.utils.constants import ErrorTypeEnum


class GraphQLException(GraphQLError):
    def __init__(self, message: str, error_type: ErrorTypeEnum):
        super().__init__(message, extensions={'error_type': error_type.value})

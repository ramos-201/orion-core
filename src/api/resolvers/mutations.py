from ariadne import MutationType
from graphql import GraphQLError

from src.api.constants import ErrorTypeEnum


mutation = MutationType()


class MutationError(GraphQLError):
    def __init__(self, message, error_type: ErrorTypeEnum):
        super().__init__(message, extensions={'error_type': error_type.value})


@mutation.field('createUser')
def resolve_create_user(
        _, info,
        name: str,
        last_name: str,
        username: str,
        email: str,
        mobile_phone: str,
        password: str,
):
    required_data = {
        'name': name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'mobile_phone': mobile_phone,
        'password': password,
    }
    missing_fields = [key for key, value in required_data.items() if value == '']

    if missing_fields:
        raise MutationError(
            message=f'The following fields cannot be empty: {missing_fields}',
            error_type=ErrorTypeEnum.EMPTY_DATA_ERROR,
        )

    data_user = {
        'id': '1',
        'name': name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'mobile_phone': mobile_phone,
        'password': password,
    }
    return {'user': data_user}


__all__ = ['mutation']

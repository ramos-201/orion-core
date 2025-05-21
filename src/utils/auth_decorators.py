from functools import wraps

from src.utils.constants import ErrorTypeEnum
from src.utils.exceptions import GraphQLException


def login_required(resolver):
    @wraps(resolver)
    async def wrapper(obj, info, **kwargs):
        if not info.context.get('user'):
            raise GraphQLException(
                message='The authentication has expired or is invalid.',
                error_type=ErrorTypeEnum.UNAUTHORIZED_ERROR,
            )
        return await resolver(obj, info, **kwargs)
    return wrapper

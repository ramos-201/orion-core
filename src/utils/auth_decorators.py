from functools import wraps

from src.utils.exceptions import UnauthorizedException


def login_required(resolver):
    @wraps(resolver)
    async def wrapper(obj, info, **kwargs):
        if not info.context.get('user'):
            raise UnauthorizedException(message='The authentication has expired or is invalid.')
        return await resolver(obj, info, **kwargs)
    return wrapper

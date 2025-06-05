from functools import wraps

from src.controllers.user_controller import UserController
from src.utils.exceptions import UnauthorizedException
from src.utils.jwt_handler import decode_access_token


def login_required(resolver):
    @wraps(resolver)
    async def wrapper(obj, info, **kwargs):
        request = info.context.get('request')
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            raise UnauthorizedException(message='Authentication token is missing or invalid.')

        token = auth_header.removeprefix('Bearer ').strip()
        user_id = decode_access_token(token=token)

        if not user_id:
            raise UnauthorizedException(message='Invalid or expired authentication token.')

        user = await UserController().get_user_by_id(user_id=user_id)

        if not user:
            raise UnauthorizedException(message='Authenticated user does not exist.')

        info.context['user'] = user
        return await resolver(obj, info, **kwargs)

    return wrapper

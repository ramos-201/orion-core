from starlette.requests import Request

from src.controllers.user_controller import UserController
from src.utils.jwt_handler import decode_access_token


async def get_context(request: Request) -> dict:
    context = {
        'request': request,
        'user_id': None,
        'user': None,
    }
    header = request.headers.get('Authorization', '')

    if header.startswith('Bearer '):
        token = header.split(' ', 1)[1]
        user_id = decode_access_token(token=token)
        context['user_id'] = user_id

        if user_id:
            user_controller = UserController()
            user = await user_controller.get_user_by_id(user_id=user_id)
            context['user'] = user

    return context

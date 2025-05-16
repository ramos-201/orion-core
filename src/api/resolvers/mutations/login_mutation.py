from src.api.resolvers.payload import user_to_dict
from src.constants import ErrorTypeEnum
from src.controllers.user_controller import UserController
from src.exceptions import MutationError
from src.utils.jwt_handler import create_access_token
from src.utils.validate_data import validate_required_data


async def resolve_login(
    _, info,
    user: str,
    password: str,
) -> dict:
    validate_required_data(
        user=user,
        password=password,
    )

    user_controller = UserController()

    user = await user_controller.get_user_by_credentials(user=user, password=password)
    if not user:
        raise MutationError(
            message='The credentials entered are not valid.',
            error_type=ErrorTypeEnum.INVALID_CREDENTIALS_ERROR,
        )

    token = create_access_token(user.id)
    return {
        'user': user_to_dict(user=user),
        'token': token,
    }

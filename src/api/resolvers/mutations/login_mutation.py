from src.constants import ErrorTypeEnum
from src.controllers.user_controller import UserController
from src.exceptions import MutationError
from src.utils import validate_required_data


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

    user_result = {
        'id': '1',
        'username': 'john.smith',
    }

    return {'user': user_result}

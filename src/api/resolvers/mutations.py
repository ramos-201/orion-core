from ariadne import MutationType
from graphql import GraphQLError

from src.api.constants import ErrorTypeEnum
from src.controllers.user_controller import UserController


mutation = MutationType()


class MutationError(GraphQLError):
    def __init__(self, message: str, error_type: ErrorTypeEnum):
        super().__init__(message, extensions={'error_type': error_type.value})


def validate_required_data(**kwargs) -> None:
    missing_fields = [key for key, value in kwargs.items() if value == '']
    if missing_fields:
        raise MutationError(
            message=f'The following fields cannot be empty: {missing_fields}',
            error_type=ErrorTypeEnum.EMPTY_DATA_ERROR,
        )


@mutation.field('createUser')
async def resolve_create_user(
        _, info,
        name: str,
        last_name: str,
        username: str,
        email: str,
        mobile_phone: str,
        password: str,
) -> dict:
    validate_required_data(
        name=name,
        last_name=last_name,
        username=username,
        email=email,
        mobile_phone=mobile_phone,
        password=password,
    )
    user_controller = UserController()
    user_created = await user_controller.create_user(
        name=name,
        last_name=last_name,
        username=username,
        email=email,
        mobile_phone=mobile_phone,
        password=password,
    )

    user_result = {
        'id': user_created.id,
        'username': user_created.username,
    }

    return {'user': user_result}


__all__ = ['mutation']

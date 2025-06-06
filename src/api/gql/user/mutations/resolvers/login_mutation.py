from typing import Any

from src.api.gql.user.types.payloads.user_payload_type import UserPayloadType
from src.controllers.user_controller import UserController
from src.utils.exceptions import InvalidCredentialException
from src.utils.jwt_handler import create_access_token
from src.utils.validate_data import validate_not_empty_fields


login_type_gql = """
login(
    user: String!
    password: String!
): UserPayloadType
"""


async def resolve_login(
    _, info,
    user: str,
    password: str,
) -> dict[str, Any]:
    validate_not_empty_fields(
        user=user,
        password=password,
    )

    user_controller = UserController()

    user_obj = await user_controller.get_user_by_credentials(user=user, password=password)

    if not user_obj:
        raise InvalidCredentialException(message='The credentials entered are not valid.')

    token = create_access_token(user_id=user_obj.id)

    return UserPayloadType.to_result(user=user_obj, token=token)

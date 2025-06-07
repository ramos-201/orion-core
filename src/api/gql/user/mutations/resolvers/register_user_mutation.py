from typing import Any

from src.api.gql.user.types.payloads.user_payload_type import UserPayloadType
from src.controllers.user_controller import UserController
from src.utils.jwt_handler import create_access_token
from src.utils.validate_data import validate_not_empty_fields


register_user_type_gql = """
registerUser(
    name: String!
    lastName: String!
    username: String!
    email: String!
    mobilePhone: String!
    password: String!
): UserPayloadType
"""


async def resolve_register_user(
    _, info,
    name: str,
    last_name: str,
    username: str,
    email: str,
    mobile_phone: str,
    password: str,
) -> dict[str, Any]:
    validate_not_empty_fields(
        name=name,
        last_name=last_name,
        username=username,
        email=email,
        mobile_phone=mobile_phone,
        password=password,
    )

    user_controller = UserController()

    user = await user_controller.create_user(
        name=name,
        last_name=last_name,
        username=username,
        email=email,
        mobile_phone=mobile_phone,
        password=password,
    )

    token = create_access_token(user_id=user.id)

    return UserPayloadType.to_result(user=user, token=token)

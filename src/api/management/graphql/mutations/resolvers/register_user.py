from typing import Any

from src.api.management.graphql.payloads.user_payload_type import UserPayloadType


register_user_type_gql = """
registerUser(
    name: String!,
    lastName: String!,
    username: String!,
    email: String!,
    mobilePhone: String!,
    password: String!
): UserPayloadType
"""


def resolve_register_user(
    _, info,
    name: str,
    last_name: str,
    username: str,
    email: str,
    mobile_phone: str,
    password: str,
) -> dict[str, Any]:
    user = {
        'id': '1',
        'name': name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'mobile_phone': mobile_phone,
        'password': password,
    }
    return UserPayloadType.to_result(user=user, token='<PASSWORD>')

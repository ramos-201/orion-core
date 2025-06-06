from typing import Any

from src.api.gql.user.types.schemes_type.user_type import UserType
from src.api.gql.utils.graphql_type_abs import GraphQLTypeAbs
from src.models import User


class UserPayloadType(GraphQLTypeAbs):
    type_def_gql = """
    type UserPayloadType {
        user: UserType!
        token: String!
    }
    """

    @classmethod
    def to_result(cls, user: User, token: str) -> dict[str, Any]:
        return {
            'user': UserType.to_result(user),
            'token': token,
        }

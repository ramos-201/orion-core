from typing import Any

from src.api.management.graphql.graphql_type_abs import GraphQLTypeAbs
from src.api.management.graphql.schemas_type.user_type import UserType


class UserPayloadType(GraphQLTypeAbs):
    type_def_gql = """
    type UserPayloadType {
        user: UserType!
        token: String!
    }
    """

    @classmethod
    def to_result(cls, user: dict[str, str], token: str) -> dict[str, Any]:
        return {
            'user': UserType.to_result(user),
            'token': token,
        }

from src.api.management.graphql.graphql_type_abs import GraphQLTypeAbs
from src.models import User


class UserType(GraphQLTypeAbs):
    type_def_gql = """
    type UserType {
        id: String
        username: String
        name: String
        email: String
        mobilePhone: String
    }
    """

    @classmethod
    def to_result(cls, user: User) -> dict[str, str]:
        return {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'mobile_phone': user.mobile_phone,
        }

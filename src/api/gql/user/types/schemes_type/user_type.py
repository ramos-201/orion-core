from src.api.gql.utils.graphql_type_abs import GraphQLTypeAbs
from src.models import User


class UserType(GraphQLTypeAbs):
    type_def_gql = """
    type UserType {
        username: String!
        name: String!
        lastName: String!
        email: String!
        mobilePhone: String!
    }
    """

    @classmethod
    def to_result(cls, user: User) -> dict[str, str]:
        return {
            'username': user.username,
            'name': user.name,
            'last_name': user.last_name,
            'email': user.email,
            'mobile_phone': user.mobile_phone,
        }

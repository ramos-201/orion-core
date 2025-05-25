from src.api.management.graphql.graphql_type_abs import GraphQLTypeAbs


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
    def to_result(cls, user: dict[str, str]) -> dict[str, str]:
        return {
            'id': user['id'],
            'username': user['username'],
            'name': user['name'],
            'email': user['email'],
            'mobile_phone': user['mobile_phone'],
        }

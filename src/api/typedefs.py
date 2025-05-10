from ariadne import gql


user_type_def = """
type User {
    id: String!
    username: String!
}
"""

auth_payload_type_def = """
type AuthPayload {
    user: User
}
"""

query_type_def = """
type Query {
    _empty: String
}
"""

mutation_type_def = """
type Mutation {
    createUser(
        name: String!,
        lastName: String!,
        username: String!,
        email: String!,
        mobilePhone: String!,
        password: String!
    ): AuthPayload

    login(
        user: String!,
        password: String!
    ): AuthPayload
}
"""

type_defs = gql(query_type_def + mutation_type_def + user_type_def + auth_payload_type_def)

__all__ = ['type_defs']

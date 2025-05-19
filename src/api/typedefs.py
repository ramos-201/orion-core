from ariadne import gql


schema_type_def = """
type User {
    id: String!
    username: String!
    name: String!
    email: String!
    mobilePhone: String!
}

type Process {
    id: String!
    createdAt: String!
    modifiedAt: String!
    name: String!
    description: String
}
"""

payload_type_def = """
type UserPayload {
    user: User!
}

type AuthPayload {
    user: User!
    token: String!
}

type ProcessPayload {
    process: Process!
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
    ): UserPayload

    login(
        user: String!,
        password: String!
    ): AuthPayload

    createProcess(
        name: String!
        description: String
    ): ProcessPayload
}
"""

type_defs = gql(query_type_def + mutation_type_def + schema_type_def + payload_type_def)

__all__ = ['type_defs']

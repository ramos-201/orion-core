from ariadne import (
    gql,
    make_executable_schema,
)

from src.api.mutations import mutation
from src.api.queries import query


type_defs = gql("""
    type Query {
        hello: String!
    }

    type Mutation {
        setMessageHello(
            message: String!
        ): String!
    }
""")

schema = make_executable_schema(type_defs, query, mutation)

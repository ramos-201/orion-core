from ariadne import gql
from ariadne_graphql_modules import ObjectType


class EmptyQuery(ObjectType):
    __schema__ = gql("""
    type Query {
        _empty: Boolean!
    }
    """)

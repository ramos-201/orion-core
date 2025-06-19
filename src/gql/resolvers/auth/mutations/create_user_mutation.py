from ariadne import gql
from ariadne_graphql_modules import MutationType


class CreateUserMutation(MutationType):
    __schema__ = gql("""
        type Mutation {
            createUser: String!
        }
    """)

    @staticmethod
    async def resolve_mutation(_, info):
        return 'Hello'

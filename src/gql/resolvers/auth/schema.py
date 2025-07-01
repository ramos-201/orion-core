from ariadne_graphql_modules import (
    CollectionType,
    make_executable_schema,
)

from src.gql.resolvers.auth.mutations import (
    AuthenticationMutation,
    CreateAccountMutation,
)
from src.gql.resolvers.auth.queries import EmptyQuery


class AccountMutations(CollectionType):
    __types__ = [
        CreateAccountMutation,
        AuthenticationMutation,
    ]


schema = make_executable_schema(EmptyQuery, AccountMutations)

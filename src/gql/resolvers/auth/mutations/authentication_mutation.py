from ariadne import gql
from ariadne_graphql_modules import (
    InputType,
    MutationType,
    convert_case,
)

from src.controllers.account_controller import AccountController
from src.gql.schemes.payload import AccountPayload


class AuthenticationInput(InputType):
    __schema__ = """
    input AuthenticationInput {
        user: String!
        password: String!
    }
    """


class AuthenticationMutation(MutationType):
    __schema__ = gql("""
    type Mutation {
        authentication(
            authenticationData: AuthenticationInput!
        ): AccountPayload!
    }
    """)
    __requires__ = [AuthenticationInput, AccountPayload]
    __args__ = convert_case

    @staticmethod
    async def resolve_mutation(_, info, authentication_data: AuthenticationInput) -> dict:
        user = authentication_data['user']
        password = authentication_data['password']

        account_controller = AccountController()
        account = await account_controller.get_account(user=user, password=password)

        return AccountPayload.to_result(account=account, token='')


__all__ = ['AuthenticationMutation']

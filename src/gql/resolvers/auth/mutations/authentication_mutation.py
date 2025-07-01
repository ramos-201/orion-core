from ariadne import gql
from ariadne_graphql_modules import (
    InputType,
    MutationType,
    convert_case,
)

from src.controllers.account_controller import AccountController
from src.gql.schemes.payload import AccountPayload
from src.utils.jwt_handler import create_access_token


class AuthenticationInput(InputType):
    __schema__ = """
    input AuthenticationInput {
        identifier: String!
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
        identifier = authentication_data['identifier']
        password = authentication_data['password']

        account_controller = AccountController()
        account = await account_controller.get_account_by_credentials(identifier=identifier, password=password)

        token = create_access_token(account_id=account.id)

        return AccountPayload.to_result(account=account, token=token)


__all__ = ['AuthenticationMutation']

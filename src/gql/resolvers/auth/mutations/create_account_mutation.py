from ariadne import gql
from ariadne_graphql_modules import (
    InputType,
    MutationType,
    convert_case,
)

from src.controllers.account_controller import AccountController
from src.gql.schemes.types import AccountType
from src.utils.data_validator import validate_not_empty_fields


class AccountInput(InputType):
    __schema__ = """
    input AccountInput {
        email: String!
        username: String!
        password: String!
    }
    """


class CreateAccountMutation(MutationType):
    __schema__ = gql("""
    type Mutation {
        createAccount(
            accountData: AccountInput!
        ): AccountType!
    }
    """)
    __requires__ = [AccountInput, AccountType]
    __args__ = convert_case

    @staticmethod
    async def resolve_mutation(_, info, account_data: AccountInput) -> dict:
        email = account_data['email']
        username = account_data['username']
        password = account_data['password']

        validate_not_empty_fields(
            email=email,
            username=username,
            password=password,
        )

        account_controller = AccountController()

        account = await account_controller.create_account(
            email=email,
            username=username,
            password=password,
        )

        return AccountType.to_result(account=account)


__all__ = ['CreateAccountMutation']

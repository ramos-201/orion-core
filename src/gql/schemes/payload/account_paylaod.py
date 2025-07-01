from ariadne_graphql_modules import ObjectType

from src.gql.schemes.types import AccountType
from src.gql.schemes.types.base_abs import ResultGQLBase
from src.models import Account


class AccountPayload(ObjectType, ResultGQLBase):
    __schema__ = """
    type AccountPayload {
        account: AccountType
        token: String
    }
    """
    __requires__ = [AccountType]

    @classmethod
    def to_result(cls, account: Account, token: str) -> dict:
        return {
            'account': AccountType.to_result(account=account),
            'token': token,
        }

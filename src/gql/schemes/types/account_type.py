from ariadne_graphql_modules import ObjectType

from src.gql.schemes.types.base_abs import ResultGQLBase
from src.models import Account


class AccountType(ObjectType, ResultGQLBase):
    __schema__ = """
    type AccountType {
        email: String
        username: String
    }
    """

    @classmethod
    def to_result(cls, account: Account) -> dict:
        return {
            'email': account.email,
            'username': account.username,
        }

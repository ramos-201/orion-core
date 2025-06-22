from pytest import mark

from src.main import AUTH_GQL_ENDPOINT
from src.models import Account


mutation = """
mutation createAccount(
    $accountData: AccountInput!
) {
    createAccount(
        accountData: $accountData
    ) {
        email
        username
    }
}
"""


variables = {
    'accountData': {
        'email': 'john.smith@example.cpm',
        'username': 'john,smith',
        'password': 'password',
    },
}


@mark.asyncio
async def test_create_account_mutation_successfully(initialize_db, client):
    response = client.post(AUTH_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    account_data = variables['accountData']

    assert response_json == {
        'data': {
            'createAccount': {
                'email': account_data['email'],
                'username': account_data['username'],
            },
        },
    }

    account = await Account.get(username=account_data['username'])

    assert account.email == account_data['email']
    assert account.username == account_data['username']

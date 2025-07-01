from pytest import mark
from pytest_asyncio import fixture

from src.main import AUTH_GQL_ENDPOINT


mutation = """
mutation authentication(
    $authenticationData: AuthenticationInput!
) {
    authentication(
        authenticationData: $authenticationData
    ) {
        account {
            email
            username
        }
        token
    }
}
"""


@fixture
def variables(default_account_constructor):
    return {
        'authenticationData': {
            'user': 'name user example',
            'password': 'password example',
        },
    }


@mark.asyncio
async def test_authentication_mutation_successfully(client, variables, default_account_constructor):
    variables['authenticationData']['user'] = default_account_constructor.email
    variables['authenticationData']['password'] = default_account_constructor.password

    response = await client.post(AUTH_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    # account_data = variables['accountData']

    assert response_json == {'data': {'authentication': {'account': {'email': '', 'username': ''}, 'token': ''}}}

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
            'identifier': 'name user example',
            'password': 'password example',
        },
    }


@mark.parametrize(
    'identifier_key', (
        'email',
        'username',
    ),
)
@mark.asyncio
async def test_authentication_mutation_successfully(
    client, variables, default_account_constructor, mocker, identifier_key,
):
    token_mock = 'token_example.mock'
    mocker.patch(
        'src.gql.resolvers.auth.mutations.authentication_mutation.create_access_token',
        return_value=token_mock,
    )

    variables['authenticationData']['identifier'] = getattr(default_account_constructor, identifier_key)
    variables['authenticationData']['password'] = default_account_constructor.password

    response = await client.post(AUTH_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()

    assert response_json == {
        'data': {
            'authentication': {
                'account': {
                    'email': default_account_constructor.email,
                    'username': default_account_constructor.username,
                },
                'token': token_mock,
            },
        },
    }

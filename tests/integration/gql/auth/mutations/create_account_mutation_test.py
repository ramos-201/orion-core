from pytest import mark
from pytest_asyncio import fixture

from src.enums.error_type_enum import ErrorTypeEnum
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


@fixture
def variables():
    return {
        'accountData': {
            'email': 'john.smith@example.cpm',
            'username': 'john,smith',
            'password': 'password',
        },
    }


@mark.asyncio
async def test_create_account_mutation_successfully(client, variables):
    response = await client.post(AUTH_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
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


@mark.parametrize(
    'email_field, username_field, expected_field_result', (
        ('email', '__not_found__', 'email'),
        ('__not_found__', 'username', 'username'),
    ),
)
@mark.asyncio
async def test_create_account_mutation_when_unique_fields_exist_in_account_model_returns_duplicate_field_error(
    client, default_account_constructor, variables, email_field, username_field, expected_field_result,
):
    variables['accountData']['email'] = getattr(default_account_constructor, email_field, 'new_email@example.com')
    variables['accountData']['username'] = getattr(default_account_constructor, username_field, 'new_username_example')
    variables['accountData']['password'] = default_account_constructor.password

    response = await client.post(AUTH_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()

    assert response_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': f'The data for the field "{expected_field_result}" already exists.',
            'details': {
                'value': expected_field_result,
            },
        }],
    }


@mark.asyncio
async def test_register_account_mutation_with_empty_required_variables_returns_empty_data_error(client, variables):
    variables['accountData']['email'] = ''
    variables['accountData']['username'] = ''
    variables['accountData']['password'] = ''

    response = await client.post(AUTH_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: ["email", "username", "password"].',
            'details': {},
        }],
    }

from pytest import mark

from src.api.router_api import USER_GQL_ENDPOINT
from src.utils.constants import ErrorTypeEnum


mutation = """
mutation login(
    $identifier: String!
    $password: String!
) {
    login(
        identifier: $identifier
        password: $password
    ) {
        user {
            username
            name
            email
            mobilePhone
        }
        token
    }
}
"""


@mark.asyncio
@mark.parametrize(
    'user_field', (
        'email',
        'username',
    ),
)
async def test_login_successfully(
    client, initialize_db, default_user_registration_constructor, mocker, user_field,
):
    token_mock = 'token_example.mock'
    mocker.patch(
        'src.api.gql.user.mutations.resolvers.login_mutation.create_access_token',
        return_value=token_mock,
    )

    variables = {
        'identifier': getattr(default_user_registration_constructor, user_field),
        'password': default_user_registration_constructor.password,
    }

    response = client.post(USER_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'login': {
                'user': {
                    'username': default_user_registration_constructor.username,
                    'name': default_user_registration_constructor.name,
                    'email': default_user_registration_constructor.email,
                    'mobilePhone': default_user_registration_constructor.mobile_phone,
                },
                'token': token_mock,
            },
        },
    }


def test_login_with_null_required_variables_returns_internal_error(client):
    variables = {
        'identifier': None,
        'password': None,
    }

    response = client.post(USER_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': None,
        'errors': [
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable "$identifier" of non-null type "String!" must not be null.',
            }, {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable "$password" of non-null type "String!" must not be null.',
            },
        ],
    }


def test_login_with_empty_required_variables_returns_empty_data_error(client):
    variables = {
        'identifier': '',
        'password': '',
    }

    response = client.post(USER_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'login': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: ["identifier", "password"].',
        }],
    }


@mark.asyncio
@mark.parametrize(
    'password_field, user_field', (
        ('password', '__not_found__'),
        ('__not_found__', 'username'),
        ('__not_found__', 'email'),
        ('__not_found__', '__not_found__'),
    ),
)
async def test_login_with_invalid_credentials_returns_invalid_credentials_error(
    client, initialize_db, default_user_registration_constructor, password_field, user_field,
):
    variables = {
        'identifier': getattr(default_user_registration_constructor, user_field, 'user_not_exist'),
        'password': getattr(default_user_registration_constructor, password_field, 'wrong_password'),
    }

    response = client.post(USER_GQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'login': None},
        'errors': [{
            'error_type': ErrorTypeEnum.INVALID_CREDENTIALS_ERROR.value,
            'message': 'The credentials entered are not valid.',
        }],
    }

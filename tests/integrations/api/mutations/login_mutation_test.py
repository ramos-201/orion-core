from pytest import mark

from src.api.graphql.router import ENDPOINT_NAME
from src.utils.constants import ErrorTypeEnum


mutation = """
mutation login(
    $user: String!,
    $password: String!
) {
    login(
        user: $user,
        password: $password
    ) {
        user {
            id
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
async def test_login_success(client_api, initialize_db, default_user_registration_constructor, user_field, monkeypatch):
    token_mock = 'token_example.mock'
    monkeypatch.setattr(
        'src.api.graphql.resolvers.mutations.login_mutation.create_access_token',
        lambda user_id: token_mock,
    )

    variables = {
        'user': getattr(default_user_registration_constructor, user_field),
        'password': default_user_registration_constructor.password,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {
            'login': {
                'token': token_mock,
                'user': {
                    'id': str(default_user_registration_constructor.id),
                    'username': default_user_registration_constructor.username,
                    'name': default_user_registration_constructor.name,
                    'email': default_user_registration_constructor.email,
                    'mobilePhone': default_user_registration_constructor.mobile_phone,
                },
            },
        },
    }


def test_login_fails_with_null_data(client_api):
    variables = {
        'user': None,
        'password': None,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': None,
        'errors': [
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $user of non-null type String! must not be null.',
            },
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $password of non-null type String! must not be null.',
            },
        ],
    }


def test_login_fails_with_empty_fields(client_api):
    variables = {
        'user': '',
        'password': '',
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {'login': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: [user, password].',
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
async def test_fails_due_to_invalid_credentials(
    client_api, initialize_db, default_user_registration_constructor, password_field, user_field,
):
    variables = {
        'user': getattr(default_user_registration_constructor, user_field, 'user_not_exist'),
        'password': getattr(default_user_registration_constructor, password_field, 'wrong_password'),
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {'login': None},
        'errors': [{
            'error_type': ErrorTypeEnum.INVALID_CREDENTIALS_ERROR.value,
            'message': 'The credentials entered are not valid.',
        }],
    }

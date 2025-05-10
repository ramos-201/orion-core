from pytest import mark

from src.constants import (
    ENDPOINT_NAME,
    ErrorTypeEnum,
)


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
        }
    }
}
"""


@mark.asyncio
@mark.parametrize(
    'user', (
        'john.smith',
        'john.smith@example.com',
    ),
)
async def test_login_success(client_api, initialize_db, default_user_registration_constructor, user):
    created_user = await default_user_registration_constructor
    variables = {
        'user': user,
        'password': created_user.password,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {
            'login': {
                'user': {
                    'id': str(created_user.id),
                    'username': created_user.username,
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
    'password, user', (
        ('password.example', 'username_not_exist'),
        ('wrong_password', 'username_not_exist'),
        ('wrong_password', 'john.smith'),
        ('wrong_password', 'john.smith@example.com'),
    ),
)
async def test_fails_due_to_invalid_credentials(
    client_api, initialize_db, default_user_registration_constructor,
    password, user,
):
    created_user = await default_user_registration_constructor
    variables = {
        'user': 'user_no_exist',
        'password': created_user.password,
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

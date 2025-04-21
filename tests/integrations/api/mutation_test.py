from src.api.constants import (
    ENDPOINT_NAME,
    ErrorTypeEnum,
)


mutation = """
        mutation CreateUser(
            $name: String!,
            $lastName: String!,
            $username: String!,
            $email: String!,
            $mobilePhone: String!,
            $password: String!
        ) {
            createUser(
                name: $name,
                lastName: $lastName,
                username: $username,
                email: $email,
                mobilePhone: $mobilePhone,
                password: $password
            ) {
                user {
                    id
                    username
                }
            }
        }
    """


def test_create_user_success(client_api):
    variables = {
        'name': 'jon',
        'lastName': 'smith',
        'username': 'jon.smith',
        'email': 'jon.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password.example',
    }

    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
    )
    data_json = response.json()

    assert data_json == {
        'data': {
            'createUser': {
                'user': {
                    'id': '1',
                    'username': 'jon.smith',
                },
            },
        },
    }


def test_create_user_error_with_null_data(client_api):
    variables = {
        'name': None,
        'lastName': None,
        'username': None,
        'email': None,
        'mobilePhone': None,
        'password': None,
    }

    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
    )
    data_json = response.json()

    assert data_json == {
        'data': None,
        'errors': [
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $name of non-null type String! must not be null.',
            },
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $lastName of non-null type String! must not be null.',
            },
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $username of non-null type String! must not be null.',
            },
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $email of non-null type String! must not be null.',
            },
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $mobilePhone of non-null type String! must not be null.',
            },
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $password of non-null type String! must not be null.',
            },
        ],
    }


def test_create_user_error_with_empty_fields(client_api):
    variables = {
        'name': '',
        'lastName': '',
        'username': '',
        'email': '',
        'mobilePhone': '',
        'password': '',
    }

    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
    )
    data_json = response.json()

    assert data_json == {
        'data': {
            'createUser': None,
        },
        'errors': [
            {
                'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
                'message': 'The following fields cannot be empty: [name, last_name, username, email, '
                           'mobile_phone, password]',
            },
        ],
    }

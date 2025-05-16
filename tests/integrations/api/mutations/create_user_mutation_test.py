from pytest import mark

from configs import ENDPOINT_NAME
from src.constants import ErrorTypeEnum
from src.models import User


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


@mark.asyncio
async def test_create_user_success(client_api, initialize_db):
    variables = {
        'name': 'jon',
        'lastName': 'smith',
        'username': 'jon.smith',
        'email': 'jon.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password.example',
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {
            'createUser': {
                'user': {
                    'id': '1',
                    'username': variables['username'],
                },
            },
        },
    }

    user_created = await User.get(id=data_json['data']['createUser']['user']['id'])
    assert user_created.name == variables['name']
    assert user_created.last_name == variables['lastName']
    assert user_created.username == variables['username']
    assert user_created.email == variables['email']
    assert user_created.mobile_phone == variables['mobilePhone']
    assert user_created.password == variables['password']


def test_create_user_fails_with_null_data(client_api):
    variables = {
        'name': None,
        'lastName': None,
        'username': None,
        'email': None,
        'mobilePhone': None,
        'password': None,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

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


def test_create_user_fails_with_empty_fields(client_api):
    variables = {
        'name': '',
        'lastName': '',
        'username': '',
        'email': '',
        'mobilePhone': '',
        'password': '',
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {'createUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: [name, last_name, username, email, '
                       'mobile_phone, password].',
        }],
    }


@mark.asyncio
async def test_create_user_fails_when_duplicated_data(client_api, initialize_db, default_user_registration_constructor):
    created_user = await default_user_registration_constructor

    variables = {
        'name': created_user.name,
        'lastName': created_user.last_name,
        'username': created_user.username,
        'email': created_user.email,
        'mobilePhone': created_user.mobile_phone,
        'password': created_user.password,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {'createUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field mobile_phone already exists.',
        }],
    }

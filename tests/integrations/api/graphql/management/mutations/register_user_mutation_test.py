from datetime import datetime

from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT
from src.models.user import User
from src.utils.enums.type_error import ErrorTypeEnum


mutation = """
mutation registerUser(
    $name: String!,
    $lastName: String!,
    $username: String!,
    $email: String!,
    $mobilePhone: String!,
    $password: String!
) {
    registerUser(
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
            name
            email
            mobilePhone
        }
        token
    }
}
"""


@mark.asyncio
async def test_register_user_successfully(client, initialize_db):
    variables = {
        'name': 'John',
        'lastName': 'Smith',
        'username': 'john.smith',
        'email': 'john.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password_example',
    }

    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {
            'registerUser': {
                'user': {
                    'id': '1',
                    'username': variables['username'],
                    'name': variables['name'],
                    'email': variables['email'],
                    'mobilePhone': variables['mobilePhone'],
                },
                'token': '<PASSWORD>',
            },
        },
    }

    user = await User.get(id=data_json['data']['registerUser']['user']['id'])
    assert user.name == variables['name']
    assert user.last_name == variables['lastName']
    assert user.username == variables['username']
    assert user.email == variables['email']
    assert user.mobile_phone == variables['mobilePhone']
    assert user.password == variables['password']
    assert user.is_account_active
    assert type(user.created_at) is datetime
    assert type(user.modified_at) is datetime


def test_register_user_with_null_variables_returns_internal_error(client):
    variables = {
        'name': None,
        'lastName': None,
        'username': None,
        'email': None,
        'mobilePhone': None,
        'password': None,
    }

    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': None,
        'errors': [
            {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $name of non-null type String! must not be null.',
            }, {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $lastName of non-null type String! must not be null.',
            }, {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $username of non-null type String! must not be null.',
            }, {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $email of non-null type String! must not be null.',
            }, {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $mobilePhone of non-null type String! must not be null.',
            }, {
                'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
                'message': 'Variable $password of non-null type String! must not be null.',
            },
        ],
    }

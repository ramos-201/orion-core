from datetime import datetime

from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT
from src.models.user import User
from src.utils.constants import ErrorTypeEnum


mutation = """
mutation registerUser(
    $name: String!
    $lastName: String!
    $username: String!
    $email: String!
    $mobilePhone: String!
    $password: String!
) {
    registerUser(
        name: $name
        lastName: $lastName
        username: $username
        email: $email
        mobilePhone: $mobilePhone
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
async def test_register_user_successfully(client, initialize_db, mocker):
    token_mock = 'token_example.mock'
    mocker.patch(
        'src.api.management.graphql.mutations.resolvers.register_user_mutation.create_access_token',
        return_value=token_mock,
    )

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

    response_json = response.json()
    assert response_json == {
        'data': {
            'registerUser': {
                'user': {
                    'id': response_json['data']['registerUser']['user']['id'],
                    'username': variables['username'],
                    'name': variables['name'],
                    'email': variables['email'],
                    'mobilePhone': variables['mobilePhone'],
                },
                'token': token_mock,
            },
        },
    }

    user = await User.get(id=response_json['data']['registerUser']['user']['id'])
    assert user.name == variables['name']
    assert user.last_name == variables['lastName']
    assert user.username == variables['username']
    assert user.email == variables['email']
    assert user.mobile_phone == variables['mobilePhone']
    assert user.password == variables['password']
    assert user.is_account_active
    assert type(user.created_at) is datetime
    assert type(user.modified_at) is datetime


def test_register_user_with_null_required_variables_returns_internal_error(client):
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

    response_json = response.json()
    assert response_json == {
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


def test_register_user_with_empty_required_variables_returns_empty_data_error(client):
    variables = {
        'name': '',
        'lastName': '',
        'username': '',
        'email': '',
        'mobilePhone': '',
        'password': '',
    }

    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'registerUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: [name, last_name, username, email, mobile_phone, '
                       'password].',
        }],
    }


@mark.asyncio
async def test_register_user_when_unique_fields_exist_in_user_model_returns_duplicate_field_error(
    client, initialize_db, default_user_registration_constructor,
):
    variables = {
        'name': default_user_registration_constructor.name,
        'lastName': default_user_registration_constructor.last_name,
        'username': default_user_registration_constructor.username,
        'email': default_user_registration_constructor.email,
        'mobilePhone': default_user_registration_constructor.mobile_phone,
        'password': default_user_registration_constructor.password,
    }

    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'registerUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field mobile_phone already exists.',
        }],
    }

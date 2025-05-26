from datetime import datetime

from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT
from src.models.user import User


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

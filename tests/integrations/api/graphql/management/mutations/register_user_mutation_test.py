from starlette.testclient import TestClient

from src.api.router import GRAPHQL_ENDPOINT
from src.app import app


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


def test_register_user_successfully():
    client = TestClient(app)

    variables = {
        'name': 'John',
        'lastName': 'Smith',
        'username': 'john.smith',
        'email': 'john.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password_example',
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
    )

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

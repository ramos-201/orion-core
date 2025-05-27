from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT


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
async def test_login_successfully(client, initialize_db, default_user_registration_constructor, user_field):
    variables = {
        'user': getattr(default_user_registration_constructor, user_field),
        'password': default_user_registration_constructor.password,
    }
    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {
            'login': {
                'user': {
                    'id': str(default_user_registration_constructor.id),
                    'username': default_user_registration_constructor.username,
                    'name': default_user_registration_constructor.name,
                    'email': default_user_registration_constructor.email,
                    'mobilePhone': default_user_registration_constructor.mobile_phone,
                },
                'token': '<PASSWORD>',
            },
        },
    }

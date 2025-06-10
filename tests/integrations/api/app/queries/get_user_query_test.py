from pytest import mark

from src.api.router_api import APP_GQL_ENDPOINT
from src.utils.constants import ErrorTypeEnum


query = """
query getUser {
    getUser {
        username
        name
        email
        mobilePhone
    }
}
"""


@mark.asyncio
async def test_get_user_successfully(
    client, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'getUser': {
                'username': default_user_registration_constructor.username,
                'name': default_user_registration_constructor.name,
                'email': default_user_registration_constructor.email,
                'mobilePhone': default_user_registration_constructor.mobile_phone,
            },
        },
    }


@mark.asyncio
@mark.parametrize(
    'headers', (
        {},
        {'Authorization': ''},
        {'': ''},
    ),
)
async def test_get_user_with_no_authentication_return_unauthorized_error(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor, headers,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {}},
        headers=headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'getUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Authentication token is missing or invalid.',
        }],
    }


@mark.asyncio
async def test_get_user_with_expired_token_return_unauthorized_error(
    client, initialize_db, patch_expired_token, get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'getUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Invalid or expired authentication token.',
        }],
    }

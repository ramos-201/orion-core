import uuid

from pytest import mark

from src.api.router_api import APP_GQL_ENDPOINT
from src.models import User
from src.utils.constants import ErrorTypeEnum
from tests.factory_test import UserFactory


mutation = """
mutation updateUser(
    $name: String
    $lastName: String
    $mobilePhone: String
) {
    updateUser(
        name: $name
        lastName: $lastName
        mobilePhone: $mobilePhone
    ) {
        username
        name
        lastName
        email
        mobilePhone
    }
}
"""


@mark.asyncio
async def test_update_user_successfully(
    client, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    variables = {
        'name': 'New name',
        'lastName': 'New last name',
        'mobilePhone': '3122222222',
    }

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'updateUser': {
                'username': default_user_registration_constructor.username,
                'name': variables['name'],
                'lastName': variables['lastName'],
                'email': default_user_registration_constructor.email,
                'mobilePhone': variables['mobilePhone'],
            },
        },
    }

    user = await User.get(username=default_user_registration_constructor.username)

    assert user.name != default_user_registration_constructor.username
    assert user.name == variables['name']

    assert user.last_name != default_user_registration_constructor.last_name
    assert user.last_name == variables['lastName']

    assert user.mobile_phone != default_user_registration_constructor.mobile_phone
    assert user.mobile_phone == variables['mobilePhone']


@mark.parametrize(
    'name_variable, last_name_variable, mobile_phone_variable', (
        ('New Name', None, None),
        (None, 'New last name', None),
        (None, None, '3122222222'),
    ),
)
@mark.asyncio
async def test_update_user_with_null_variable_successfully(
    client, initialize_db, get_authenticated_headers, default_user_registration_constructor,
    name_variable, last_name_variable, mobile_phone_variable,
):
    variables = {
        'name': name_variable,
        'lastName': last_name_variable,
        'mobilePhone': mobile_phone_variable,
    }

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    user = await User.get(username=default_user_registration_constructor.username)

    assert user.name == variables['name'] or default_user_registration_constructor.name
    assert user.last_name == variables['lastName'] or default_user_registration_constructor.last_name
    assert user.mobile_phone == variables['mobilePhone'] or default_user_registration_constructor.mobile_phone


@mark.asyncio
async def test_update_user_with_unique_fields_exist_in_user_model_return_duplicate_field_error(
    client, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    new_user = UserFactory.build(
        id=uuid.uuid4(),
        username='New user',
        email='new_email@example.com',
        mobile_phone='3122222222',
    )
    await new_user.save()

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {'mobilePhone': new_user.mobile_phone}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    assert response.json() == {
        'data': {'updateUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field "mobile_phone" already exists.',
        }],
    }


@mark.asyncio
async def test_update_user_with_empty_variables_return_empty_data_error(
    client, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    assert response.json() == {
        'data': {'updateUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'There is no data to update.',
        }],
    }


@mark.asyncio
@mark.parametrize(
    'headers', (
        {},
        {'Authorization': ''},
        {'': ''},
    ),
)
async def test_update_user_with_no_authentication_return_unauthorized_error(
    client, initialize_db, get_authenticated_headers, headers,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {'name': 'New name'}},
        headers=headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Authentication token is missing or invalid.',
        }],
    }


@mark.asyncio
async def test_update_user_with_expired_token_return_unauthorized_error(
    client, initialize_db, patch_expired_token, get_authenticated_headers,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {'name': 'New name'}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Invalid or expired authentication token.',
        }],
    }


@mark.asyncio
def test_update_user_with_null_variables_return_empty_data_error(client, initialize_db, get_authenticated_headers):
    variables = {
        'name': None,
        'lastName': None,
        'mobilePhone': None,
    }

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateUser': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'There is no data to update.',
        }],
    }

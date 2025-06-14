from datetime import datetime

from pytest import mark
from pytest_asyncio import fixture

from src.api.router_api import APP_GQL_ENDPOINT
from src.models.process import Process
from src.utils.constants import ErrorTypeEnum


mutation = """
mutation registerProcess(
    $name: String!
    $description: String
    $isActive: Boolean
) {
    registerProcess(
        name: $name
        description: $description
        isActive: $isActive
    ) {
        id
        createdAt
        modifiedAt
        name
        description
        isActive
    }
}
"""


@fixture
def variables():
    return {
        'name': 'name process example',
        'description': 'description process example',
        'isActive': True,
    }


@mark.asyncio
@mark.parametrize(
    'description_value, is_active_value, expected_result_is_active', (
        ('This is example description.', True, True),
        (None, True, True),
        ('This is example description.', None, True),
        ('This is example description.', False, False),
        ('',  True, True),
        ('',  False, False),
        (None, None, True),
    ),
)
async def test_register_process_successfully(
    client, variables, initialize_db, get_patch_datetime_model, get_authenticated_headers,
    default_user_registration_constructor, description_value, is_active_value, expected_result_is_active,
):
    variables['description'] = description_value
    variables['isActive'] = is_active_value

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'registerProcess': {
                'id': response_json['data']['registerProcess']['id'],
                'name': variables['name'],
                'createdAt': get_patch_datetime_model,
                'modifiedAt': get_patch_datetime_model,
                'description': variables['description'],
                'isActive': expected_result_is_active,
            },
        },
    }

    process = await Process.get(id=response_json['data']['registerProcess']['id'])
    assert process.name == variables['name']
    assert process.description == variables['description']
    assert process.is_active == expected_result_is_active
    assert await process.user == default_user_registration_constructor
    assert type(process.created_at) is datetime
    assert type(process.modified_at) is datetime


@mark.asyncio
@mark.parametrize(
    'key_variables, value_variables, expected_result_is_active, expected_result_description', (
        ('description', 'This is example description.', True, 'This is example description.'),
        ('description', None, True, None),
        ('isActive', True, True, None),
        ('isActive', False, False, None),
        ('isActive', None, True, None),
    ),
)
async def test_register_process_with_data_no_required_successfully(
    client, initialize_db, get_patch_datetime_model, get_authenticated_headers,
    key_variables, value_variables, expected_result_is_active, expected_result_description,
):
    variables = {
        'name': 'name process example',
        key_variables: value_variables,
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
            'registerProcess': {
                'id': response_json['data']['registerProcess']['id'],
                'name': variables['name'],
                'createdAt': get_patch_datetime_model,
                'modifiedAt': get_patch_datetime_model,
                'description': expected_result_description,
                'isActive': expected_result_is_active,
            },
        },
    }

    process = await Process.get(id=response_json['data']['registerProcess']['id'])
    assert process is not None


@mark.asyncio
async def test_register_process_when_user_has_multiple_existing_processes_successfully(
    client, variables, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    response_process_1 = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response_process_1.status_code == 200

    variables_process_2 = {
        'name': 'name process example 2',
        'description': 'This a example description 2.',
        'isActive': True,
    }

    response_process_1 = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables_process_2},
        headers=get_authenticated_headers,
    )
    assert response_process_1.status_code == 200

    processes = await Process.filter(user_id=default_user_registration_constructor.id)
    assert len(processes) == 2

    assert processes[0].name == variables['name']
    assert processes[1].name == variables_process_2['name']


@mark.asyncio
@mark.parametrize(
    'headers', (
        {},
        {'Authorization': ''},
        {'': ''},
    ),
)
async def test_register_process_with_no_authentication_return_unauthorized_error(
    client, variables, initialize_db, get_authenticated_headers, headers,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Authentication token is missing or invalid.',
        }],
    }


@mark.asyncio
async def test_register_process_with_expired_token_return_unauthorized_error(
    client, variables, initialize_db, patch_expired_token, get_authenticated_headers,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Invalid or expired authentication token.',
        }],
    }


@mark.asyncio
def test_register_process_with_null_variables_return_internal_error(
    client, initialize_db, get_authenticated_headers,
):
    variables = {
        'name': None,
        'description': None,
        'isActive': None,
    }

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
            'message': 'Variable "$name" of non-null type "String!" must not be null.',
        }],
    }


@mark.asyncio
async def test_register_process_with_empty_variables_return_empty_data_error(
    client, initialize_db, get_authenticated_headers,
):
    variables = {
        'name': '',
        'description': '',
        'isActive': bool(''),
    }

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: ["name"].',
        }],
    }


@mark.asyncio
async def test_register_process_when_unique_fields_exist_in_process_model_returns_duplicate_field_error(
    client, variables, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    variables['name'] = default_process_registration_constructor.name
    variables['description'] = default_process_registration_constructor.description
    variables['isActive'] = default_process_registration_constructor.is_active

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field "name" already exists.',
        }],
    }

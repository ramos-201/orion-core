from datetime import datetime

from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT
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
        process {
            id
            createdAt
            modifiedAt
            name
            description
            isActive
        }
    }
}
"""


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
    client, initialize_db, get_patch_datetime_model, get_authenticated_headers, default_user_registration_constructor,
    description_value, is_active_value, expected_result_is_active,
):
    variables = {
        'name': 'name process example',
        'description': description_value,
        'isActive': is_active_value,
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {
            'registerProcess': {
                'process': {
                    'id': '1',
                    'name': variables['name'],
                    'createdAt': get_patch_datetime_model,
                    'modifiedAt': get_patch_datetime_model,
                    'description': variables['description'],
                    'isActive': expected_result_is_active,
                },
            },
        },
    }

    process = await Process.get(id=data_json['data']['registerProcess']['process']['id'])
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
        ('isActive', True, True, ''),
        ('isActive', False, False, ''),
        ('isActive', None, True, ''),
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
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {
            'registerProcess': {
                'process': {
                    'id': '1',
                    'name': variables['name'],
                    'createdAt': get_patch_datetime_model,
                    'modifiedAt': get_patch_datetime_model,
                    'description': expected_result_description,
                    'isActive': expected_result_is_active,
                },
            },
        },
    }

    process = await Process.get(id=data_json['data']['registerProcess']['process']['id'])
    assert process is not None


@mark.asyncio
@mark.parametrize(
    'headers', (
        {},
        {'Authorization': 'Bearer '},
        {'Authorization': ''},
        {'': ''},
        {'Authorization': 'Bearer invalid_token'},
    ),
)
async def test_register_process_with_no_authentication_return_unauthorized_error(
    client, initialize_db, get_authenticated_headers, headers,
):
    variables = {
        'name': 'name process example',
        'description': 'This is a example description.',
        'isActive': True,
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'The authentication has expired or is invalid.',
        }],
    }


@mark.asyncio
async def test_register_process_with_expired_token_return_unauthorized_error(
    client, initialize_db, patch_expired_token, get_authenticated_headers,
):
    variables = {
        'name': 'name process example',
        'description': 'This is a example description.',
        'isActive': True,
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'The authentication has expired or is invalid.',
        }],
    }


@mark.asyncio
def test_register_process_with_null_variables_return_internal_error(client, initialize_db, get_authenticated_headers):
    variables = {
        'name': None,
        'description': '<Optional>',
        'isActive': bool('<Optional>'),
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
            'message': 'Variable $name of non-null type String! must not be null.',
        }],
    }


@mark.asyncio
async def test_register_process_with_empty_variables_return_empty_data_error(
    client, initialize_db, get_authenticated_headers,
):
    variables = {
        'name': '',
        'description': '<Optional>',
        'isActive': bool('<Optional>'),
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: [name].',
        }],
    }


@mark.asyncio
async def test_register_process_when_unique_fields_exist_in_process_model_returns_duplicate_field_error(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    variables = {
        'name': default_process_registration_constructor.name,
        'description': default_process_registration_constructor.description,
        'isActive': default_process_registration_constructor.is_active,
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    data_json = response.json()
    assert data_json == {
        'data': {'registerProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field name already exists.',
        }],
    }

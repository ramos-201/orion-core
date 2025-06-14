import uuid

from pytest import mark
from pytest_asyncio import fixture

from src.api.router_api import APP_GQL_ENDPOINT
from src.models import Process
from src.utils.constants import ErrorTypeEnum
from tests.factory_test import ProcessFactory


mutation = """
mutation updateProcess(
    $id: String!
    $name: String
    $description: String
    $isActive: Boolean
) {
    updateProcess(
        id: $id
        name: $name
        description: $description
        isActive: $isActive
    ) {
        id
        name
        description
        isActive
    }
}
"""


@fixture
def variables():
    return {
        'name': 'New name process example',
        'description': 'New description process example',
        'isActive': False,
    }


@mark.asyncio
async def test_update_process_successfully(
    client, variables, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    variables['id'] = str(default_process_registration_constructor.id)

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'updateProcess': {
                'id': str(default_process_registration_constructor.id),
                'name': variables['name'],
                'description': variables['description'],
                'isActive': variables['isActive'],
            },
        },
    }

    process = await Process.get(id=default_process_registration_constructor.id)

    assert process.name != default_process_registration_constructor.name
    assert process.name == variables['name']

    assert process.description != default_process_registration_constructor.description
    assert process.description == variables['description']

    assert process.is_active != default_process_registration_constructor.is_active
    assert process.is_active == variables['isActive']


@mark.parametrize(
    'name_variable, description_variable, is_active_variable', (
        ('New Name', None, None),
        (None, 'New description', None),
        (None, None, False),
    ),
)
@mark.asyncio
async def test_update_process_with_null_variable_successfully(
    client, variables, initialize_db, get_authenticated_headers, default_process_registration_constructor,
    name_variable, description_variable, is_active_variable,
):
    variables['id'] = str(default_process_registration_constructor.id)
    variables['name'] = name_variable
    variables['description'] = description_variable
    variables['isActive'] = is_active_variable

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    process = await Process.get(id=default_process_registration_constructor.id)

    assert process.name == variables['name'] or default_process_registration_constructor.name
    assert process.description == variables['description'] or default_process_registration_constructor.description
    assert process.is_active == variables['isActive'] or default_process_registration_constructor.is_active


@mark.asyncio
async def test_update_process_with_unique_fields_exist_in_process_model_return_duplicate_field_error(
    client, variables, initialize_db, get_authenticated_headers, default_user_registration_constructor,
    default_process_registration_constructor,
):
    new_process = ProcessFactory.build(
        id=uuid.uuid4(),
        user=default_user_registration_constructor,
        name=variables['name'],
    )
    await new_process.save()

    variables['id'] = str(default_process_registration_constructor.id)

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    assert response.json() == {
        'data': {'updateProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field "name" already exists.',
        }],
    }


@mark.asyncio
async def test_update_process_with_not_variables_return_internal_error(
    client, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    assert response.json() == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
            'message': 'Variable "$id" of required type "String!" was not provided.',
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
async def test_update_process_with_no_authentication_return_unauthorized_error(
    client, variables, initialize_db, get_authenticated_headers,
    default_process_registration_constructor, headers,
):
    variables['id'] = str(default_process_registration_constructor.id)

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Authentication token is missing or invalid.',
        }],
    }


@mark.asyncio
async def test_update_process_with_expired_token_return_unauthorized_error(
    client, variables, initialize_db, patch_expired_token, get_authenticated_headers,
    default_process_registration_constructor,
):
    variables['id'] = str(default_process_registration_constructor.id)

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Invalid or expired authentication token.',
        }],
    }


@mark.parametrize(
    'field_variable', (
        None,
        '',
    ),
)
@mark.asyncio
async def test_update_process_with_empty_variables_return_empty_data_error(
    client, variables, initialize_db, get_authenticated_headers,
    default_process_registration_constructor, field_variable,
):
    variables['id'] = str(default_process_registration_constructor.id)
    variables['name'] = field_variable
    variables['description'] = field_variable
    variables.pop('isActive', None)

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'No valid data was submitted for update.',
        }],
    }


@mark.asyncio
async def test_update_process_with_id_not_exist_return_(
    client, variables, initialize_db, get_authenticated_headers,
    default_process_registration_constructor,
):
    variables['id'] = 'id_not_exist'

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'updateProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': f'The process for the id: "{variables['id']}" does not exist.',
        }],
    }

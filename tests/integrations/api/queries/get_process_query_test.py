from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT
from src.utils.constants import ErrorTypeEnum


query = """
query getProcess(
    $id: String
    $name: String
) {
    getProcess(
        id: $id
        name: $name
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


@mark.asyncio
@mark.parametrize(
    'key_variable, process_field', (
        ('id', 'id'),
        ('name', 'name'),
    ),
)
async def test_get_process_successfully(
    client, initialize_db, get_authenticated_headers, get_patch_datetime_model,
    default_process_registration_constructor, key_variable, process_field,
):
    variables = {key_variable: str(getattr(default_process_registration_constructor, process_field))}

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'getProcess': {
                'id': str(default_process_registration_constructor.id),
                'createdAt': get_patch_datetime_model,
                'modifiedAt': get_patch_datetime_model,
                'name': default_process_registration_constructor.name,
                'description': default_process_registration_constructor.description,
                'isActive': default_process_registration_constructor.is_active,
            },
        },
    }


@mark.asyncio
async def test_get_process_with_all_variables_successfully(
    client, initialize_db, get_authenticated_headers, get_patch_datetime_model,
    default_process_registration_constructor,
):
    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }

    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': variables},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'getProcess': {
                'id': str(default_process_registration_constructor.id),
                'createdAt': get_patch_datetime_model,
                'modifiedAt': get_patch_datetime_model,
                'name': default_process_registration_constructor.name,
                'description': default_process_registration_constructor.description,
                'isActive': default_process_registration_constructor.is_active,
            },
        },
    }


@mark.asyncio
async def test_get_process_with_other_fields_returns_null_data(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': {'other_field': 'example'}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {'data': {'getProcess': None}}


@mark.asyncio
@mark.parametrize(
    'key_field_variables', (
        'id',
        'name',
    ),
)
async def test_get_process_with_empty_fields_variables_returns_null_data(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor, key_field_variables,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': {key_field_variables: ''}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {'data': {'getProcess': None}}


@mark.asyncio
@mark.parametrize(
    'key_field_variables', (
        'id',
        'name',
    ),
)
async def test_get_process_with_null_fields_variables_returns_null_data(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor, key_field_variables,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': {key_field_variables: None}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {'data': {'getProcess': None}}


@mark.asyncio
async def test_get_process_with_empty_variables_returns_null_data(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': {}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {'data': {'getProcess': None}}


@mark.asyncio
@mark.parametrize(
    'headers', (
        {},
        {'Authorization': ''},
        {'': ''},
    ),
)
async def test_get_process_with_no_authentication_return_unauthorized_error(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor, headers,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers=headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'getProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Authentication token is missing or invalid.',
        }],
    }


@mark.asyncio
async def test_get_process_with_expired_token_return_unauthorized_error(
    client, initialize_db, patch_expired_token, get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'getProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Invalid or expired authentication token.',
        }],
    }

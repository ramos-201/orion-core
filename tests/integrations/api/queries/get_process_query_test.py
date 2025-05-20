from pytest import mark

from src.constants import ErrorTypeEnum
from src.main import ENDPOINT_NAME
from src.utils.jwt_handler import create_access_token
from tests.factory_test import UserFactory


query = """
query GetProcess(
    $id: String
    $name: String
) {
    process(
        id: $id,
        name: $name
    ) {
        id
        createdAt
        modifiedAt
        name
        description
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
async def test_get_process_by_unique_key(
        client_api, initialize_db, get_authenticated_headers, default_process_registration_constructor,
        key_variable, process_field,
):
    variables = {key_variable: str(getattr(default_process_registration_constructor, process_field))}
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {
        'data': {
            'process': {
                'id': str(default_process_registration_constructor.id),
                'createdAt': str(default_process_registration_constructor.created_at),
                'modifiedAt': default_process_registration_constructor.modified_at.strftime('%Y-%m-%d %H:%M:%S+00:00'),
                'name': default_process_registration_constructor.name,
                'description': default_process_registration_constructor.description,
            },
        },
    }


@mark.asyncio
async def test_get_process_by_unique_key_when_send_all_fields(
        client_api, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {
        'data': {
            'process': {
                'id': str(default_process_registration_constructor.id),
                'createdAt': str(default_process_registration_constructor.created_at),
                'modifiedAt': default_process_registration_constructor.modified_at.strftime('%Y-%m-%d %H:%M:%S+00:00'),
                'name': default_process_registration_constructor.name,
                'description': default_process_registration_constructor.description,
            },
        },
    }


@mark.asyncio
async def test_get_process_returns_none_if_process_belongs_to_different_user(
        client_api, initialize_db, default_process_registration_constructor,
):
    user = await UserFactory.build(
        username='name_example_get_process_fail',
        email='john.smith@example_get_process_fail.com',
        mobile_phone='3222222222',
    )
    await user.save()

    token = create_access_token(user_id=user.id)
    headers = {'Authorization': f'Bearer {token}'}

    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers=headers,
    )

    data_json = response.json()
    assert data_json == {'data': {'process': None}}


@mark.asyncio
@mark.parametrize(
    'key_variable', (
        'id',
        'name',
    ),
)
async def test_get_process_fails_with_null_key(client_api, initialize_db, get_authenticated_headers, key_variable):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {key_variable: None}},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {'data': {'process': None}}


@mark.asyncio
@mark.parametrize(
    'key_variable', (
        'id',
        'name',
    ),
)
async def test_create_process_fails_with_empty_fields(
        client_api, initialize_db, get_authenticated_headers, default_process_registration_constructor,
        key_variable,
):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {key_variable: ''}},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {'data': {'process': None}}


@mark.asyncio
async def test_get_process_null_when_process_not_exist(client_api, initialize_db, get_authenticated_headers):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': '1', 'name': 'process_not_exist'}},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {'data': {'process': None}}


expected_result_unauthorized_error = {
    'data': {'process': None},
    'errors': [{
        'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
        'message': 'The authentication has expired or is invalid.',
    }],
}


@mark.asyncio
async def test_get_process_fail_when_not_authorized(
        client_api, initialize_db, default_process_registration_constructor,
):
    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers={},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_get_process_fail_when_expired_token(
        client_api, initialize_db, default_process_registration_constructor, patch_expired_token,
        get_authenticated_headers,
):
    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_get_process_fail_when_null_token(client_api, initialize_db, default_process_registration_constructor):
    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers={'Authorization': 'Bearer '},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_get_process_fail_when_invalid_token(client_api, initialize_db, default_process_registration_constructor):
    variables = {
        'id': str(default_process_registration_constructor.id),
        'name': default_process_registration_constructor.name,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': variables},
        headers={'Authorization': 'Bearer invalid_token'},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error

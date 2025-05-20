from pytest import mark

from src.constants import ErrorTypeEnum
from src.main import ENDPOINT_NAME


query = """
query GetProcess(
    $id: String!
) {
    process(
        id: $id,
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
async def test_get_process_by_id(
        client_api, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
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
async def test_get_process_null_when_process_not_exist(client_api, initialize_db, get_authenticated_headers):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': '1'}},
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
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers={},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_get_process_fail_when_expired_token(
        client_api, initialize_db, default_process_registration_constructor, patch_expired_token,
        get_authenticated_headers,
):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_get_process_fail_when_null_token(client_api, initialize_db, default_process_registration_constructor):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers={'Authorization': 'Bearer '},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_get_process_fail_when_invalid_token(client_api, initialize_db, default_process_registration_constructor):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers={'Authorization': 'Bearer invalid_token'},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


def test_get_process_fails_with_null_id(client_api):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': None}},
        headers={},
    )

    data_json = response.json()
    assert data_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
            'message': 'Variable $id of non-null type String! must not be null.',
        }],
    }


@mark.asyncio
async def test_create_process_fails_with_empty_fields(
        client_api, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': query, 'variables': {'id': ''}},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {'data': {'process': None}}

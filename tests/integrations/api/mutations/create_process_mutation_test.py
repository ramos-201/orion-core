from pytest import mark

from src.api.graphql.router import ENDPOINT_NAME
from src.models import Process
from src.utils.constants import ErrorTypeEnum


# TODO: test, cada usuario debe tener sus propios procesos y no deberia afectar el flujo de otro usuario.


mutation = """
mutation CreateProcess(
    $name: String!,
    $description: String
) {
    createProcess(
        name: $name,
        description: $description
    ) {
        process {
            id
            createdAt
            modifiedAt
            name
            description
        }
    }
}
"""

this_is_description = 'this is a example description.'


@mark.asyncio
@mark.parametrize(
    'description_variables', [
        'this is a example description.',
        '',
        None,
    ],
)
async def test_create_process_success(
        client_api, initialize_db, get_authenticated_headers, default_user_registration_constructor,
        get_patch_datetime_model, description_variables,
):
    variables = {
        'name': 'process_example',
        'description': description_variables,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {
        'data': {
            'createProcess': {
                'process': {
                    'id': '1',
                    'name': variables['name'],
                    'createdAt': get_patch_datetime_model,
                    'modifiedAt': get_patch_datetime_model,
                    'description': variables['description'],
                },
            },
        },
    }

    process_created = await Process.get(id=data_json['data']['createProcess']['process']['id'])
    assert process_created.name == variables['name']
    assert process_created.description == variables['description']
    assert await process_created.user == default_user_registration_constructor


@mark.asyncio
async def test_create_processes_success(
        client_api, initialize_db, get_authenticated_headers, default_user_registration_constructor,
):
    variables_process_1 = {
        'name': 'process_example_1',
        'description': this_is_description,
    }
    _ = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables_process_1},
        headers=get_authenticated_headers,
    )

    variables_process_2 = {
        'name': 'process_example_2',
        'description': this_is_description,
    }
    _ = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables_process_2},
        headers=get_authenticated_headers,
    )

    processes = await Process.filter(user_id=default_user_registration_constructor.id).count()
    assert processes == 2


expected_result_unauthorized_error = {
    'data': {'createProcess': None},
    'errors': [{
        'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
        'message': 'The authentication has expired or is invalid.',
    }],
}


def test_create_process_fail_when_not_authorized(client_api):
    variables = {
        'name': 'process_example',
        'description': this_is_description,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers={},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


@mark.asyncio
async def test_create_process_fail_when_expired_token(
        client_api, initialize_db, patch_expired_token, get_authenticated_headers,
):
    variables = {
        'name': 'process_example',
        'description': this_is_description,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


def test_create_process_fail_when_null_token(client_api):
    variables = {
        'name': 'process_example',
        'description': this_is_description,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers={'Authorization': 'Bearer '},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


def test_create_process_fail_when_invalid_token(client_api):
    variables = {
        'name': 'process_example',
        'description': this_is_description,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers={'Authorization': 'Bearer invalid_token'},
    )

    data_json = response.json()
    assert data_json == expected_result_unauthorized_error


def test_create_process_fails_with_null_data(client_api):
    variables = {
        'name': None,
        'description': None,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers={},
    )

    data_json = response.json()
    assert data_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
            'message': 'Variable $name of non-null type String! must not be null.',
        }],
    }


@mark.asyncio
async def test_create_process_fails_with_empty_fields(client_api, initialize_db, get_authenticated_headers):
    variables = {
        'name': '',
        'description': '',
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {
        'data': {'createProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.EMPTY_DATA_ERROR.value,
            'message': 'The following fields cannot be empty: [name].',
        }],
    }


@mark.asyncio
async def test_create_process_fails_when_duplicated_data(
        client_api, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    variables = {
        'name': default_process_registration_constructor.name,
        'description': default_process_registration_constructor.description,
    }
    response = client_api.post(
        ENDPOINT_NAME,
        json={'query': mutation, 'variables': variables},
        headers=get_authenticated_headers,
    )

    data_json = response.json()
    assert data_json == {
        'data': {'createProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field name already exists.',
        }],
    }

from pytest import mark

from configs import ENDPOINT_NAME
from src.constants import ErrorTypeEnum
from src.models import Process


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
            name
        }
    }
}
"""


@mark.asyncio
@mark.parametrize(
    'description_variable', [
        'this is a example description.',
        '',
        None,
    ],
)
async def test_create_process_success(client_api, initialize_db, description_variable):
    variables = {
        'name': 'process_example',
        'description': description_variable,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {
            'createProcess': {
                'process': {
                    'id': '1',
                    'name': variables['name'],
                },
            },
        },
    }

    process_created = await Process.get(id=data_json['data']['createProcess']['process']['id'])
    assert process_created.name == variables['name']
    assert process_created.description == variables['description']


def test_create_process_fails_with_null_data(client_api):
    variables = {
        'name': None,
        'description': None,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': None,
        'errors': [{
            'error_type': ErrorTypeEnum.INTERNAL_ERROR.value,
            'message': 'Variable $name of non-null type String! must not be null.',
        }],
    }


def test_create_process_fails_with_empty_fields(client_api):
    variables = {
        'name': '',
        'description': '',
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

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
        client_api, initialize_db, default_process_registration_constructor,
):
    created_process = await default_process_registration_constructor

    variables = {
        'name': created_process.name,
        'description': created_process.description,
    }
    response = client_api.post(ENDPOINT_NAME, json={'query': mutation, 'variables': variables})

    data_json = response.json()
    assert data_json == {
        'data': {'createProcess': None},
        'errors': [{
            'error_type': ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value,
            'message': 'The data for the field name already exists.',
        }],
    }

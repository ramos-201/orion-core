from datetime import datetime

from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT
from src.models.process import Process


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
    client, initialize_db, get_patch_datetime_model, description_value, is_active_value, expected_result_is_active,
):
    variables = {
        'name': 'name process example',
        'description': description_value,
        'isActive': is_active_value,
    }

    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})
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
    assert await process.user is None
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
    client, initialize_db, get_patch_datetime_model, key_variables, value_variables, expected_result_is_active,
    expected_result_description,
):
    variables = {
        'name': 'name process example',
        key_variables: value_variables,
    }

    response = client.post(GRAPHQL_ENDPOINT, json={'query': mutation, 'variables': variables})
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

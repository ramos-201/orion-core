from pytest import mark

from src.constants import ENDPOINT_NAME
from src.models import Process


mutation = """
mutation CreateProcess(
    $name: String!,
    $description: String!
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
async def test_create_process_success(client_api, initialize_db):
    variables = {
        'name': 'process_example',
        'description': 'this is a example description.',
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

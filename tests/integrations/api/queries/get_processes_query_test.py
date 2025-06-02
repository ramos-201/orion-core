from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT


query = """
query getProcesses(
    $isActive: Boolean
    $limit: Int
    $offset: Int
) {
    getProcesses(
        isActive: $isActive
        limit: $limit
        offset: $offset
    ) {
        total
        processes {
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
}
"""


@mark.asyncio
async def test_get_processes_when_variables_are_not_sent_successfully(
    client, initialize_db, get_patch_datetime_model, default_user_registration_constructor,
    get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        GRAPHQL_ENDPOINT,
        json={'query': query, 'variables': None},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {
            'getProcesses': {
                'total': 1,
                'processes': [{
                    'process': {
                        'id': str(default_process_registration_constructor.id),
                        'createdAt': get_patch_datetime_model,
                        'modifiedAt': get_patch_datetime_model,
                        'name': default_process_registration_constructor.name,
                        'description': default_process_registration_constructor.description,
                        'isActive': default_process_registration_constructor.is_active,
                    },
                }],
            },
        },
    }

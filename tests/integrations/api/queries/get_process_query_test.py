from pytest import mark

from src.api.router_api import GRAPHQL_ENDPOINT


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

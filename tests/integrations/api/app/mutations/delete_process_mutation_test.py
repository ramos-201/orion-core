from pytest import mark

from src.api.router_api import APP_GQL_ENDPOINT
from src.models import (
    BackupData,
    Process,
)


mutation = """
mutation deleteProcess(
    $id: String!
) {
    deleteProcess(
        id: $id
    )
}
"""


@mark.asyncio
async def test_delete_process_successfully(
    client, initialize_db, get_patch_datetime_model, get_authenticated_headers,
    default_process_registration_constructor, default_user_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {'id': str(default_process_registration_constructor.id)}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {'data': {'deleteProcess': True}}

    exist_process = await Process.get_or_none(id=default_process_registration_constructor.id)
    assert not exist_process

    backup_data = await BackupData.get_or_none(original_id=default_process_registration_constructor.id)
    assert backup_data.user_id == default_user_registration_constructor.id
    assert backup_data.object_name == default_process_registration_constructor.__class__.__name__

    """
    '{"created_at": "2025-01-01 12:00:00+00:00", "modified_at": "2025-01-01 12:00:00+00:00", '
    '"id": "6f63cfe1-d10c-4db7-94c3-8423fe3753d8", "user_id": "df1c9c0f-91fb-412d-8482-c74c0de0566c", '
    '"is_active": true, "description": "This is a example description.", "name": "name process example"}'
    """
    assert backup_data.payload is not None

    assert backup_data.metadata == {'name': f'{default_process_registration_constructor.name}'}
    assert backup_data.deleted_at

# TODO: Eliminar un id que no existe

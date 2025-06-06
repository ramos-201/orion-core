import uuid

from pytest import mark

from src.api.router_api import APP_GQL_ENDPOINT
from src.utils.constants import ErrorTypeEnum
from tests.factory_test import ProcessFactory


query = """
query getProcesses(
    $isActive: Boolean
    $limit: Int
    $pagination: Int
) {
    getProcesses(
        isActive: $isActive
        limit: $limit
        pagination: $pagination
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
@mark.parametrize(
    'variables', (
        None,
        {},
    ),
)
async def test_get_processes_when_variables_are_not_sent_successfully(
    client, initialize_db, get_patch_datetime_model,  get_authenticated_headers,
    default_process_registration_constructor, variables,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': variables},
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


@mark.asyncio
async def test_get_processes_when_there_is_more_one_record_successfully(
    client, initialize_db, default_user_registration_constructor, get_authenticated_headers,
):
    process_1 = await ProcessFactory.build(
        id=uuid.uuid4(),
        name='process_1',
        user=default_user_registration_constructor,
    )
    await process_1.save()

    process_2 = await ProcessFactory.build(
        id=uuid.uuid4(),
        name='process_2',
        user=default_user_registration_constructor,
    )
    await process_2.save()

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': None},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['data']['getProcesses']['total'] == 2
    assert len(response_json['data']['getProcesses']['processes']) == 2


@mark.asyncio
@mark.parametrize(
    'is_active_value', (
        True,
        False,
    ),
)
async def test_get_processes_with_variables_successfully(
    client, initialize_db, default_user_registration_constructor, get_authenticated_headers, is_active_value,
):
    process_obj = await ProcessFactory.build(
        user=default_user_registration_constructor,
        is_active=is_active_value,
    )
    await process_obj.save()

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'isActive': is_active_value}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['data']['getProcesses']['total'] == 1

    data_process = response_json['data']['getProcesses']['processes'][0]['process']
    assert data_process['id'] == str(process_obj.id)
    assert data_process['name'] == process_obj.name
    assert data_process['isActive'] == process_obj.is_active


@mark.asyncio
async def test_get_processes_with_pagination_successfully(
    client, initialize_db, default_user_registration_constructor, get_authenticated_headers,
):
    process_1 = await ProcessFactory.build(
        id=uuid.uuid4(),
        name='process_1',
        user=default_user_registration_constructor,
    )
    await process_1.save()

    process_2 = await ProcessFactory.build(
        id=uuid.uuid4(),
        name='process_2',
        user=default_user_registration_constructor,
    )
    await process_2.save()

    response_1 = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'limit': 2, 'pagination': 0}},
        headers=get_authenticated_headers,
    )
    assert response_1.status_code == 200

    response_1_json = response_1.json()
    assert response_1_json['data']['getProcesses']['total'] == 2
    assert len(response_1_json['data']['getProcesses']['processes']) == 2

    response_2 = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'limit': 2, 'pagination': 1}},
        headers=get_authenticated_headers,
    )
    assert response_2.status_code == 200

    response_2_json = response_2.json()
    assert response_2_json['data']['getProcesses'] is None


@mark.asyncio
async def test_get_processes_null_when_not_exist(
    client, initialize_db, default_user_registration_constructor, get_authenticated_headers,
):
    process_obj = await ProcessFactory.build(
        user=default_user_registration_constructor,
        is_active=True,
    )
    await process_obj.save()

    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'isActive': False}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {'data': {'getProcesses': None}}


@mark.asyncio
async def test_get_processes_when_null_variables_successfully(
    client, initialize_db, default_user_registration_constructor, get_authenticated_headers,
    default_process_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'isActive': None, 'limit': None, 'pagination': None}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['data']['getProcesses']['total'] == 1

    expected_process_id = response_json['data']['getProcesses']['processes'][0]['process']['id']
    assert expected_process_id == str(default_process_registration_constructor.id)


@mark.asyncio
async def test_get_processes_with_other_fields_successfully(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'other_field': 'example'}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json['data']['getProcesses']['total'] == 1


@mark.asyncio
@mark.parametrize(
    'headers', (
        {},
        {'Authorization': ''},
        {'': ''},
    ),
)
async def test_get_processes_with_no_authentication_return_unauthorized_error(
    client, initialize_db, get_authenticated_headers, default_process_registration_constructor, headers,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'isActive': default_process_registration_constructor.is_active}},
        headers=headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'getProcesses': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Authentication token is missing or invalid.',
        }],
    }


@mark.asyncio
async def test_get_processes_with_expired_token_return_unauthorized_error(
    client, initialize_db, patch_expired_token, get_authenticated_headers, default_process_registration_constructor,
):
    response = client.post(
        APP_GQL_ENDPOINT,
        json={'query': query, 'variables': {'isActive': default_process_registration_constructor.is_active}},
        headers=get_authenticated_headers,
    )
    assert response.status_code == 200

    response_json = response.json()
    assert response_json == {
        'data': {'getProcesses': None},
        'errors': [{
            'error_type': ErrorTypeEnum.UNAUTHORIZED_ERROR.value,
            'message': 'Invalid or expired authentication token.',
        }],
    }

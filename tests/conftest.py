from datetime import datetime

import pytest_asyncio
from pytest import fixture
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.main import app
from src.utils.jwt_handler import create_access_token
from tests.factory_test import (
    ProcessFactory,
    UserFactory,
)


@fixture
def client_api():
    return TestClient(app)


@pytest_asyncio.fixture
async def initialize_db():
    await Tortoise.init(
        db_url='sqlite://:memory:',
        modules={'models': ['src.models']},
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@fixture
def get_patch_datetime_model(mocker):
    default_datetime = datetime(2025, 1, 1, 12, 0, 0)
    mocker.patch('tortoise.timezone.now', return_value=default_datetime)
    return default_datetime.strftime('%Y-%m-%d %H:%M:%S')


@pytest_asyncio.fixture
async def default_user_registration_constructor(get_patch_datetime_model):
    user = await UserFactory.build(created_at=get_patch_datetime_model, modified_at=get_patch_datetime_model)
    await user.save()
    return user


@pytest_asyncio.fixture
async def default_process_registration_constructor(default_user_registration_constructor, get_patch_datetime_model):
    process = await ProcessFactory.build(
        user=default_user_registration_constructor,
        created_at=get_patch_datetime_model,
        modified_at=get_patch_datetime_model,
    )
    await process.save()
    return process


@pytest_asyncio.fixture
async def default_processes_registration_constructor(
        default_user_registration_constructor, default_process_registration_constructor, get_patch_datetime_model,
):
    process = await ProcessFactory.build(
        name='process_example_2',
        user=default_user_registration_constructor,
        created_at=get_patch_datetime_model,
        modified_at=get_patch_datetime_model,
    )
    await process.save()
    return {'process_1': default_process_registration_constructor, 'process_2': process}


@pytest_asyncio.fixture
async def get_authenticated_headers(default_user_registration_constructor, monkeypatch):
    # Authenticates with the `login` mutation.
    token = create_access_token(user_id=default_user_registration_constructor.id)
    return {'Authorization': f'Bearer {token}'}


@fixture
def patch_expired_token(monkeypatch):
    monkeypatch.setattr(
        'src.utils.jwt_handler.ACCESS_TOKEN_EXPIRE_MINUTES_TOKEN',
        '-1',
    )

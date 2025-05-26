from datetime import datetime

import pytest_asyncio
from pytest import fixture
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.app import app
from tests.factory_test import UserFactory


@fixture
def client():
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
async def default_user_registration_constructor(initialize_db, get_patch_datetime_model):
    user = await UserFactory.build(
        created_at=get_patch_datetime_model,
        modified_at=get_patch_datetime_model,
    )
    await user.save()
    return user

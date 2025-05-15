import pytest_asyncio
from pytest import fixture
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.main import app
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
async def default_user_registration_constructor():
    user = await UserFactory.build()
    await user.save()
    return user


@fixture
async def default_process_registration_constructor():
    process = await ProcessFactory.build()
    await process.save()
    return process


@fixture
def get_default_token_mock(monkeypatch):
    return


@fixture
def patch_expired_token(monkeypatch):
    monkeypatch.setattr(
        'src.utils.jwt_handler.ACCESS_TOKEN_EXPIRE_MINUTES_TOKEN',
        '-1',
    )

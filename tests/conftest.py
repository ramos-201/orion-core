import pytest_asyncio
from pytest import fixture
from starlette.testclient import TestClient
from tortoise import Tortoise

from src.main import app


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
def client():
    return TestClient(app)

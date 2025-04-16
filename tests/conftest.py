from pytest import fixture
from starlette.testclient import TestClient

from src.main import app


@fixture
def client_api():
    return TestClient(app)

from starlette.testclient import TestClient

from src.main import (
    AUTH_GQL_ENDPOINT,
    app,
)


def test_create_user_mutation_successfully():
    mutation = """
    mutation {
        createUser
    }
    """
    client = TestClient(app)

    response = client.post(
        AUTH_GQL_ENDPOINT,
        json={'query': mutation, 'variables': {}},
    )

    assert response.status_code == 200
    assert response.json() == [True, {'data': {'createUser': 'Hello'}}]

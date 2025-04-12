from starlette.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_hello_query():
    query = {
        'query': """
            query {
                hello
            }
        """,
    }

    response = client.post('/graphql', json=query)
    data = response.json()

    assert response.status_code == 200
    assert data['data']['hello'] == 'Result query, hello.'


def test_set_message_mutation():
    query = {
        'query': """
            mutation($msg: String!) {
                setMessageHello(message: $msg)
            }
        """,
        'variables': {'msg': 'Hello world'},
    }

    response = client.post('/graphql', json=query)
    data = response.json()

    assert response.status_code == 200
    assert data['data']['setMessageHello'] == 'Result mutation, set message hello: Hello world.'

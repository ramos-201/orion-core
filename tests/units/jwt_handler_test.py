import uuid

from src.utils.jwt_handler import (
    create_access_token,
    decode_access_token,
)


user_id = uuid.uuid4()


def test_create_access_token_success():
    token = create_access_token(user_id=user_id)
    assert token is not None
    assert type(token) is str


def test_decode_access_token():
    token = create_access_token(user_id=user_id)
    assert token != user_id

    decoded = decode_access_token(token=token)
    assert decoded == str(user_id)


def test_decode_expired_token(patch_expired_token):
    token = create_access_token(user_id=user_id)
    assert decode_access_token(token) is None


def test_decode_invalid_token_fail():
    assert decode_access_token(token='invalid_token') is None

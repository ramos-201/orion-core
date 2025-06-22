import uuid

from factory import Factory

from src.models import Account


DEFAULT_DATETIME = '2025-01-01 12:00:00+00:00'


class AccountFactory(Factory):
    class Meta:
        model = Account

    id = uuid.uuid4()
    created_at = DEFAULT_DATETIME
    modified_at = DEFAULT_DATETIME
    username = 'john.smith'
    email = 'john.smith@example.com'
    password = 'password.example'

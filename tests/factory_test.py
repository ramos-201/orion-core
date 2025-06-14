import uuid

from factory import (
    Factory,
    SubFactory,
)

from src.models import User
from src.models.process import Process


DEFAULT_DATETIME = '2025-01-01 12:00:00+00:00'


class UserFactory(Factory):
    class Meta:
        model = User

    id = uuid.uuid4()
    created_at = DEFAULT_DATETIME
    modified_at = DEFAULT_DATETIME
    name = 'John'
    last_name = 'Smith'
    username = 'john.smith'
    email = 'john.smith@example.com'
    mobile_phone = '3111111111'
    password = 'password.example'
    is_account_active = True


class ProcessFactory(Factory):
    class Meta:
        model = Process

    id = uuid.uuid4()
    created_at = DEFAULT_DATETIME
    modified_at = DEFAULT_DATETIME
    user = SubFactory(UserFactory)
    name = 'name process example'
    description = 'This is a example description.'
    is_active = True

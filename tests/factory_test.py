from factory import (
    Factory,
    SubFactory,
)

from src.models import (
    Process,
    User,
)


class UserFactory(Factory):
    class Meta:
        model = User

    created_at = '2025-01-01'
    modified_at = '2025-01-01'
    name = 'John'
    last_name = 'Smith'
    username = 'john.smith'
    email = 'john.smith@example.com'
    mobile_phone = '3111111111'
    password = 'password.example'


class ProcessFactory(Factory):
    class Meta:
        model = Process

    created_at = '2025-01-01'
    modified_at = '2025-01-01'
    user = SubFactory(UserFactory)
    name = 'process_example'
    description = 'this is a example description.'

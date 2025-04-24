from factory import Factory

from src.models import User


class UserFactory(Factory):
    class Meta:
        model = User

    id = '1'
    created_at = '2025-01-01'
    modified_at = '2025-01-01'
    name = 'John'
    last_name = 'Smith'
    username = 'john.smith'
    email = 'john.smith@example.com'
    mobile_phone = '3111111111'
    password = 'password.example'

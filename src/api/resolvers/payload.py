from src.models import (
    Process,
    User,
)


def user_to_dict(user: 'User') -> dict:
    return {
        'id': str(user.id),
        'username': user.username,
    }


def process_to_dict(process: 'Process') -> dict:
    return {
        'id': str(process.id),
        'name': process.name,
    }

from src.models import (
    Process,
    User,
)


def user_to_dict(user: 'User') -> dict:
    return {
        'id': str(user.id),
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'mobile_phone': user.mobile_phone,
    }


def process_to_dict(process: 'Process') -> dict:
    return {
        'id': str(process.id),
        'created_at': process.created_at,
        'modified_at': process.modified_at,
        'name': process.name,
        'description': process.description,
    }

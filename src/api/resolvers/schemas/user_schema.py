from src.models import User


def user_to_dict(user: 'User') -> dict:
    return {
        'id': str(user.id),
        'username': user.username,
    }

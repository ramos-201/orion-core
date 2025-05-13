def user_to_dict(user) -> dict:
    return {
        'id': str(user.id),
        'username': user.username,
    }

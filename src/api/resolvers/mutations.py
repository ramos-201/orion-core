from ariadne import MutationType


mutation = MutationType()


@mutation.field('createUser')
def resolve_create_user(
        _, info,
        name: str,
        last_name: str,
        username: str,
        email: str,
        mobile_phone: str,
        password: str,
):
    data_user = {
        'id': '1',
        'name': name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'mobile_phone': mobile_phone,
        'password': password,
    }
    return {'user': data_user}


__all__ = ['mutation']

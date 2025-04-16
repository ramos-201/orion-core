from ariadne import ObjectType


user_type = ObjectType('User')
auth_payload_type = ObjectType('AuthPayload')


@user_type.field('id')
def resolve_user_id(obj, _):
    return obj.get('id')


@user_type.field('username')
def resolve_user_username(obj, _):
    return obj.get('username')


@auth_payload_type.field('user')
def resolve_auth_payload_user(obj, _):
    return obj.get('user')


__all__ = ['user_type', 'auth_payload_type']

from tortoise import (
    fields,
    models,
)


# TODO: activate, desactivate user user.
# TODO: rol?

class User(models.Model):
    id = fields.IntField(pk=True, auto=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=120)
    last_name = fields.CharField(max_length=120)
    username = fields.CharField(max_length=120, unique=True)
    email = fields.CharField(max_length=120, unique=True)
    mobile_phone = fields.CharField(max_length=120, unique=True)
    password = fields.CharField(max_length=120)

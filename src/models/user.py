import uuid

from tortoise import (
    fields,
    models,
)


class User(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=120)
    last_name = fields.CharField(max_length=120)
    username = fields.CharField(max_length=120, unique=True)
    email = fields.CharField(max_length=120, unique=True)
    mobile_phone = fields.CharField(max_length=120, unique=True)
    password = fields.CharField(max_length=120)
    is_account_active = fields.BooleanField(default=False)

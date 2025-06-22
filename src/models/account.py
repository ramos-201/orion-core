import uuid

from tortoise import (
    Model,
    fields,
)


class Account(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    email = fields.CharField(max_length=120, unique=True)
    username = fields.CharField(max_length=120, unique=True)
    password = fields.CharField(max_length=120)

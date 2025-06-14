import uuid

from tortoise import (
    Model,
    fields,
)


class Process(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField(
        'models.User',
        related_name='processes',
        on_delete=fields.CASCADE,
        null=True,
    )
    name = fields.CharField(max_length=120, unique=True)
    description = fields.CharField(max_length=120, null=True)
    is_active = fields.BooleanField(default=True)

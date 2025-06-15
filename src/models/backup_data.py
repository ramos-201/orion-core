import uuid

from tortoise import (
    Model,
    fields,
)


class BackupData(Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    user = fields.ForeignKeyField(
        'models.User',
        related_name='backup_data',
        on_delete=fields.CASCADE,
        null=True,
    )
    original_id = fields.UUIDField(unique=True)
    object_name = fields.CharField(max_length=120)
    payload = fields.JSONField()
    metadata = fields.JSONField(null=True)
    deleted_at = fields.DatetimeField()

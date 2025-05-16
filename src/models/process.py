from tortoise import (
    fields,
    models,
)


class Process(models.Model):
    id = fields.IntField(pk=True, auto=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=120, unique=True)
    description = fields.CharField(max_length=120, null=True)

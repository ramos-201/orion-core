from typing import Any

from tortoise.exceptions import IntegrityError
from tortoise.models import MODEL

from src.utils.exceptions import (
    DuplicateFieldException,
    EmptyDataException,
)
from src.utils.format_date import get_current_datetime
from src.utils.validate_data import is_value_null_or_empty


class InstanceHelper:
    def __init__(self, instance: MODEL):
        self._instance = instance

    async def save_instance(self) -> None:
        try:
            await self._instance.save()
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldException(message=f'The data for the field "{field_name}" already exists.')

    def apply_updates(self, fields: dict[str, Any]) -> None:
        has_update = False
        for field, value in fields.items():
            if not is_value_null_or_empty(value):
                setattr(self._instance, field, value)
                has_update = True

        if not has_update:
            raise EmptyDataException('No valid data was submitted for update.')

        self._instance.modified_at = get_current_datetime()

    def to_dict(self) -> dict[str, Any]:
        return {
            field: getattr(self._instance, field)
            for field in self._instance._meta.db_fields
        }

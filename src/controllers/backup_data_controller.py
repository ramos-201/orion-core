import json
from typing import (
    Any,
    Optional,
)

from tortoise import Model

from src.controllers.utils.base_controller import BaseController
from src.controllers.utils.instance_helper import InstanceHelper
from src.models import User
from src.models.backup_data import BackupData
from src.utils.format_date import get_current_datetime


class BackupDataController(BaseController):
    def __init__(self, user: Optional[User] = None):
        super().__init__(model=BackupData, user=user)

    async def create_backup_data(
        self,
        instance: Model,
        metadata: Optional[dict[str, Any]] = None,
    ) -> BackupData:
        instance_helper = InstanceHelper(instance)
        data = json.dumps(instance_helper.to_dict(), default=str),

        original_id = instance.id
        object_name = instance.__class__.__name__

        return await self._create(
            original_id=original_id,
            object_name=object_name,
            metadata=metadata,
            payload=data,
            deleted_at=get_current_datetime(),
        )

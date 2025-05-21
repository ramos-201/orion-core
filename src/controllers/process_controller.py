from typing import Optional

from src.controllers.base_controller import BaseController
from src.models import (
    Process,
    User,
)
from src.utils.constants import STR_OR_NONE


class ProcessController(BaseController):
    def __init__(self):
        super().__init__(model=Process)

    async def create_process(
        self,
        name: str,
        description: STR_OR_NONE,
        user: 'User',
    ) -> Process:
        return await self._create(
            name=name,
            description=description,
            user=user,
        )

    async def get_process_by_unique_key(
            self,
            user_id: int,
            id: STR_OR_NONE = None,
            name: STR_OR_NONE = None,
    ) -> Optional[Process]:
        if id:
            return await self._get_or_none(id=id, user_id=user_id)
        if name:
            return await self._get_or_none(name=name, user_id=user_id)
        return None

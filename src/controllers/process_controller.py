from typing import Optional

from src.controllers.base_controller import BaseController
from src.models import User
from src.models.process import Process


class ProcessController(BaseController):
    def __init__(self, user: Optional[User] = None):
        super().__init__(model=Process, user=user)

    async def create_process(
            self,
            name: str,
            description: Optional[str] = '',
            is_active: Optional[bool] = True,
    ) -> Process:

        if is_active is None:
            is_active = True

        return await self._create(
            name=name,
            description=description,
            is_active=is_active,
        )

    async def get_process_by_id(self, id: Optional[str] = None) -> Optional[Process]:
        return await self._get_or_none(id=id)

    async def get_process_by_name(self, name: Optional[str] = None) -> Optional[Process]:
        return await self._get_or_none(name=name)

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
            description: Optional[str],
            is_active: Optional[bool],
    ) -> Process:
        if is_active is None:
            is_active = True

        return await self._create(
            name=name,
            description=description,
            is_active=is_active,
        )

    async def get_process_by_id(self, id: str) -> Optional[Process]:
        return await self._get_or_none(id=id)

    async def get_process_by_name(self, name: str) -> Optional[Process]:
        return await self._get_or_none(name=name)

    async def get_all(self, limit: int, pagination: int) -> tuple[list[Process], int]:
        return await self._filter(limit=limit, pagination=pagination)

    async def filter_by_is_active(
        self,
        is_active: bool,
        limit: int,
        pagination: int,
    ) -> tuple[Optional[list[Process]], int]:
        return await self._filter(is_active=is_active, limit=limit, pagination=pagination)

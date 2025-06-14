from typing import Optional

from src.controllers.base_controller import (
    BaseController,
    apply_valid_updates_or_fail,
    safe_save,
)
from src.models import User
from src.models.process import Process
from src.utils.exceptions import EmptyDataException
from src.utils.format_date import get_current_datetime


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

    async def get_process_by_id(self, process_id: str) -> Optional[Process]:
        return await self._get_by_id(id=process_id)

    async def get_process_by_name(self, name: str) -> Optional[Process]:
        return await self._get_or_none(name=name)

    async def filter_processes_by_is_active(
        self,
        is_active: bool,
        limit: int,
        page: int,
    ) -> tuple[list[Process], int]:
        return await self._filter(is_active=is_active, limit=limit, page=page)

    async def get_all_processes(self, limit: int, page: int) -> tuple[list[Process], int]:
        return await self._filter(limit=limit, page=page)

    async def update_process(
            self,
            process_id: str,
            name: Optional[str],
            description: Optional[str],
            is_active: Optional[bool],
    ) -> Process:
        process = await self.get_process_by_id(process_id=process_id)

        if not process:
            raise EmptyDataException(f'The process for the id: "{process_id}" does not exist.')

        fields_to_update = {
            'name': name,
            'description': description,
            'is_active': is_active,
        }
        apply_valid_updates_or_fail(fields_to_update, process)

        process.modified_at = get_current_datetime()
        await safe_save(instance=process)

        return process

from typing import Optional

from tortoise.transactions import in_transaction

from src.controllers.backup_data_controller import BackupDataController
from src.controllers.utils.base_controller import BaseController
from src.controllers.utils.exceptions import EmptyDataNotExistIdException
from src.controllers.utils.instance_helper import InstanceHelper
from src.models import User
from src.models.process import Process
from src.utils.exceptions import DuplicateFieldException


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
            raise EmptyDataNotExistIdException(id=process_id)

        instance_helper = InstanceHelper(instance=process)
        fields_to_update = {
            'name': name,
            'description': description,
            'is_active': is_active,
        }
        instance_helper.apply_updates(fields=fields_to_update)

        await instance_helper.save_instance()

        return process

    async def delete_process(self, process_id: str) -> bool:
        process = await self.get_process_by_id(process_id=process_id)

        if not process:
            raise EmptyDataNotExistIdException(id=process_id)

        async with in_transaction() as connection:
            backup_data_controller = BackupDataController(user=self._user)
            try:
                backup_data = bool(
                    await backup_data_controller.create_backup_data(
                        instance=process,
                        metadata={'name': process.name},
                    ),
                )
            except DuplicateFieldException:
                backup_data = True

            if backup_data:
                await process.delete(using_db=connection)
                return True
        return False

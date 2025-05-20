from src.constants import STR_OR_NONE
from src.controllers.base_controller import BaseController
from src.models import (
    Process,
    User,
)


class ProcessController(BaseController):
    def __init__(self):
        super().__init__(model=Process)

    async def create_process(
        self,
        name: str,
        description: STR_OR_NONE,
        user: 'User',
    ) -> 'Process':
        return await self._create(
            name=name,
            description=description,
            user=user,
        )

    async def get_process_by_id(self, id):
        return await self._get_or_none(id=id)

from typing import Optional

from src.controllers.base_controller import BaseController
from src.models.process import Process


class ProcessController(BaseController):
    def __init__(self):
        super().__init__(model=Process)

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

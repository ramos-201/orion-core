from src.controllers.base_controller import BaseController
from src.models import Process


class ProcessController(BaseController):
    def __init__(self):
        super().__init__(model=Process)

    async def create_process(
            self,
            name,
            description,
    ) -> 'Process':
        return await self._create(
            name=name,
            description=description,
        )

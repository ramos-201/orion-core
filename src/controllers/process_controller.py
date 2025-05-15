from src.models import Process


class ProcessController:
    def __init__(self):
        self._model = Process

    async def create_process(
            self,
            name,
            description,
    ) -> 'Process':
        return await self._model.create(
            name=name,
            description=description,
        )

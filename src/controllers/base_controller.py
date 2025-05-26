from abc import (
    ABC,
    abstractmethod,
)


class BaseController(ABC):
    @abstractmethod
    def __init__(self, model):
        self._model = model

    async def _create(self, **kwargs):
        return await self._model.create(**kwargs)

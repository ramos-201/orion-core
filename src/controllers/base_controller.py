from abc import (
    ABC,
    abstractmethod,
)

from tortoise.exceptions import IntegrityError

from src.utils.exceptions import DuplicateFieldException


class BaseController(ABC):
    @abstractmethod
    def __init__(self, model):
        self._model = model

    async def _create(self, **kwargs):
        try:
            return await self._model.create(**kwargs)
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldException(message=f'The data for the field "{field_name}" already exists.')

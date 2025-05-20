from abc import (
    ABC,
    abstractmethod,
)

from tortoise.exceptions import IntegrityError

from src.constants import ErrorTypeEnum
from src.exceptions import MutationError


class BaseController(ABC):
    @abstractmethod
    def __init__(self, model):
        self._model = model

    async def _create(self, **kwargs):
        try:
            return await self._model.create(**kwargs)
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise MutationError(
                message=f'The data for the field "{field_name}" already exists.',
                error_type=ErrorTypeEnum.DUPLICATE_FIELD_ERROR,
            )

    async def _get_or_none(self, *args, **kwargs):
        try:
            return await self._model.get_or_none(*args, **kwargs)
        except ValueError:
            return None

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Optional,
)

from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q
from tortoise.models import MODEL

from src.utils.exceptions import DuplicateFieldException


class BaseController(ABC):
    @abstractmethod
    def __init__(self, model: MODEL):
        self._model = model

    async def _create(self, **kwargs: Any) -> MODEL:
        try:
            return await self._model.create(**kwargs)
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldException(message=f'The data for the field "{field_name}" already exists.')

    async def _get_or_none(self, *args: Q, **kwargs: Any) -> Optional[MODEL]:
        try:
            return await self._model.get_or_none(*args, **kwargs)
        except ValueError:
            return None

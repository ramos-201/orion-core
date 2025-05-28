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

from src.models import User
from src.utils.exceptions import DuplicateFieldException


class BaseController(ABC):
    @abstractmethod
    def __init__(self, model: MODEL, user: Optional[User] = None):
        self.user = user
        self._model = model

    def _inject_user_in_kwargs_if_exists(self, **kwargs: Any):
        if self.user:
            kwargs['user'] = self.user
        return kwargs

    async def _create(self, **kwargs: Any) -> MODEL:
        try:
            kwargs_query = self._inject_user_in_kwargs_if_exists(**kwargs)
            return await self._model.create(**kwargs_query)
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldException(message=f'The data for the field "{field_name}" already exists.')

    async def _get_or_none(self, *args: Q, **kwargs: Any) -> Optional[MODEL]:
        try:
            return await self._model.get_or_none(*args, **kwargs)
        except ValueError:
            return None

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
        self._user = user
        self._model = model

    def _inject_user_in_kwargs_if_exists(self, **kwargs: Any) -> dict[str, Any]:
        if self._user:
            kwargs['user'] = self._user
        return kwargs

    async def _create(self, **kwargs: Any) -> MODEL:
        inject_kwargs = self._inject_user_in_kwargs_if_exists(**kwargs)

        try:
            # TODO: validate not null fields
            return await self._model.create(**inject_kwargs)
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldException(message=f'The data for the field "{field_name}" already exists.')

    async def _get_or_none(self, *args: Q, **kwargs: Any) -> Optional[MODEL]:
        try:
            inject_kwargs = self._inject_user_in_kwargs_if_exists(**kwargs)
            return await self._model.get_or_none(*args, **inject_kwargs)
        except ValueError:
            return None

    async def _get_by_id(self, id: str) -> Optional[User]:
        return await self._get_or_none(id=id)

    async def _filter(
        self,
        limit: int,
        page: int,
        *args: Q,
        **kwargs: Any,
    ) -> tuple[list[MODEL], int]:
        inject_kwargs = self._inject_user_in_kwargs_if_exists(**kwargs)
        query = self._model.filter(*args, **inject_kwargs)

        offset = page * limit
        results = await query.offset(offset).limit(limit)
        total = await query.count()

        return results, total

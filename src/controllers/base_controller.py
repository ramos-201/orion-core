import re
from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q
from tortoise.models import MODEL

from src.utils.exception import DuplicateFieldException


class BaseController(ABC):
    @abstractmethod
    def __init__(self, model: MODEL):
        self.model = model

    async def _create(self, **kwargs: Any) -> MODEL:
        try:
            return await self.model.create(**kwargs)
        except IntegrityError as error:
            match = re.search(r'Key \((.*?)\)=', str(error))
            field_name = match.group(1) if match else 'unknown'
            raise DuplicateFieldException(
                message=f'The data for the field "{field_name}" already exists.',
                value=field_name,
            )

    async def _get_or_none(self, *args: Q, **kwargs: Any) -> MODEL:
        return await self.model.get_or_none(*args, **kwargs)

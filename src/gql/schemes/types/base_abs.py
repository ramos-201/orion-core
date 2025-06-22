from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class ResultGQLBase(ABC):
    @classmethod
    @abstractmethod
    def to_result(cls, *args: Any, **kwargs: Any) -> dict:
        pass

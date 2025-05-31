from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Any,
    Optional,
)


class GraphQLTypeAbs(ABC):
    @property
    @abstractmethod
    def type_def_gql(self) -> str:
        pass

    @type_def_gql.setter
    @abstractmethod
    def type_def_gql(self, value: str) -> None:
        pass

    @classmethod
    @abstractmethod
    def to_result(cls, *values: Any, **kwargs: Any) -> Optional[dict[str, Any]]:
        pass

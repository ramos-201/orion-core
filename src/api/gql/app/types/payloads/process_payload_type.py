from typing import Any

from src.api.gql.app.types.schemes_type.process_type import ProcessType
from src.api.gql.utils.graphql_type_abs import GraphQLTypeAbs
from src.models import Process


class ProcessPayloadType(GraphQLTypeAbs):
    type_def_gql = """
    type ProcessPayloadType {
        process: ProcessType!
    }
    """

    @classmethod
    def to_result(cls, process: Process) -> dict[str, Any]:
        return {'process': ProcessType.to_result(process=process)}

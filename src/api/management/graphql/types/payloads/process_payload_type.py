from typing import Any

from src.api.management.graphql.types.graphql_type_abs import GraphQLTypeAbs
from src.api.management.graphql.types.schemas_type.process_type import ProcessType
from src.models.process import Process


class ProcessPayloadType(GraphQLTypeAbs):
    type_def_gql = """
    type ProcessPayloadType {
        process: ProcessType!
    }
    """

    @classmethod
    def to_result(cls, process: Process) -> dict[str, Any]:
        return {'process': ProcessType.to_result(process)}

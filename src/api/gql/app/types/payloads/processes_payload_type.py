from typing import Any

from src.api.gql.app.types.payloads.process_payload_type import (
    ProcessPayloadType,
)
from src.api.gql.utils.graphql_type_abs import GraphQLTypeAbs
from src.models import Process


class ProcessesPayloadType(GraphQLTypeAbs):
    type_def_gql = """
    type ProcessesPayloadType {
        processes: [ProcessPayloadType!]!
        total: Int!
    }
    """

    @classmethod
    def to_result(cls, total: int, processes: list[Process]) -> dict[str, Any]:
        result_processes = []

        for process_obj in processes:
            result_process = ProcessPayloadType.to_result(process=process_obj)
            result_processes.append(result_process)

        return {
            'processes': result_processes,
            'total': total,
        }

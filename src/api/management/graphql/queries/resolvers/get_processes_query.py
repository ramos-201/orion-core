from typing import (
    Any,
    Optional,
)

from src.api.management.graphql.types.payloads.processes_payload_type import (
    ProcessesPayloadType,
)
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.auth_decorators import login_required


get_processes_type_gql = """
getProcesses(
    isActive: Boolean
    limit: Int
    offset: Int
): ProcessesPayloadType
"""


@login_required
async def resolve_get_processes(
    _, info,
    is_active: Optional[bool] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Optional[dict[str, Any]]:
    # Get data by `User`
    user_obj: User = info.context['user']

    process_controller = ProcessController(user=user_obj)

    if is_active is None:
        limit = limit or 10
        offset = offset or 0

        process_obj, total = await process_controller.get_all(limit=limit, offset=offset)

        if process_obj:
            return ProcessesPayloadType.to_result(processes=process_obj, total=total)

    return None

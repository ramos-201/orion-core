from typing import (
    Any,
    Optional,
)

from src.api.gql.app.types.payloads.processes_payload_type import (
    ProcessesPayloadType,
)
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.login_required import login_required


get_processes_type_gql = """
getProcesses(
    isActive: Boolean
    limit: Int
    page: Int
): ProcessesPayloadType
"""


@login_required
async def resolve_get_processes(
    _, info,
    is_active: Optional[bool] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
) -> Optional[dict[str, Any]]:
    # Get data by `User`
    user: User = info.context['user']

    process_controller = ProcessController(user=user)

    limit = limit or 10
    page = page or 0

    if is_active is not None:
        processes, total = await process_controller.filter_processes_by_is_active(
            is_active=is_active,
            limit=limit,
            page=page,
        )
    else:
        processes, total = await process_controller.get_all_processes(limit=limit, page=page)

    if not processes:
        return None

    return ProcessesPayloadType.to_result(total=total, processes=processes)

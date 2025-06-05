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
    pagination: Int
): ProcessesPayloadType
"""


@login_required
async def resolve_get_processes(
    _, info,
    is_active: Optional[bool] = None,
    limit: Optional[int] = None,
    pagination: Optional[int] = None,
) -> Optional[dict[str, Any]]:
    # Get data by `User`
    user_obj: User = info.context['user']

    process_controller = ProcessController(user=user_obj)

    limit = limit or 10
    pagination = pagination or 0

    if is_active is not None:
        processes_obj, total = await process_controller.filter_by_is_active(
            is_active=is_active,
            limit=limit,
            pagination=pagination,
        )
    else:
        processes_obj, total = await process_controller.get_all(limit=limit, pagination=pagination)

    if not processes_obj:
        return None

    return ProcessesPayloadType.to_result(total=total, processes=processes_obj)

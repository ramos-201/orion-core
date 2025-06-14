from typing import (
    Any,
    Optional,
)

from src.api.gql.app.types.schemes_type.process_type import ProcessType
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.login_required import login_required


get_process_type_gql = """
getProcess(
    id: String
    name: String
): ProcessType
"""


@login_required
async def resolve_get_process(
    _, info,
    id: Optional[str] = None,
    name: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    # Get data by `User`
    user: User = info.context['user']

    process_controller = ProcessController(user=user)

    process = None

    if id:
        process = await process_controller.get_process_by_id(process_id=id)
    elif name:
        process = await process_controller.get_process_by_name(name=name)

    if not process:
        return None

    return ProcessType().to_result(process=process)

from typing import (
    Any,
    Optional,
)

from src.api.gql.app.types.schemes_type.process_type import ProcessType
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.login_required import login_required


update_process_type_gql = """
updateProcess(
    id: String!
    name: String
    description: String
    isActive: Boolean
): ProcessType
"""


@login_required
async def resolve_update_process(
    _, info,
    id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> dict[str, Any]:

    # Get data by `User`
    user: User = info.context['user']

    process_controller = ProcessController(user=user)
    updated_process = await process_controller.update_process(
        process_id=id,
        name=name,
        description=description,
        is_active=is_active,
    )

    return ProcessType.to_result(process=updated_process)

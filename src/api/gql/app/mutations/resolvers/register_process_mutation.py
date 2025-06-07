from typing import (
    Any,
    Optional,
)

from src.api.gql.app.types.schemes_type.process_type import ProcessType
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.login_required import login_required
from src.utils.validate_data import validate_not_empty_fields


register_process_type_gql = """
registerProcess(
    name: String!
    description: String
    isActive: Boolean
): ProcessType
"""


@login_required
async def resolve_register_process(
    _, info,
    name: str,
    description: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> dict[str, Any]:
    validate_not_empty_fields(name=name)

    # Create data by `User`
    user: User = info.context['user']

    process_controller = ProcessController(user=user)

    process = await process_controller.create_process(
        name=name,
        description=description,
        is_active=is_active,
    )

    return ProcessType.to_result(process=process)

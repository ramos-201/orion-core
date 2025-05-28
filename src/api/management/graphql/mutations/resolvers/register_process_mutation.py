from typing import (
    Any,
    Optional,
)

from src.api.management.graphql.types.payloads.process_payload_type import (
    ProcessPayloadType,
)
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.auth_decorators import login_required
from src.utils.validate_data import validate_not_empty_fields


register_process_type_gql = """
registerProcess(
    name: String!
    description: String
    isActive: Boolean
): ProcessPayloadType
"""


@login_required
async def resolve_register_process(
    _, info,
    name: str,
    description: Optional[str] = '',
    is_active: Optional[bool] = True,
) -> dict[str, Any]:
    validate_not_empty_fields(name=name)

    user: User = info.context['user']

    process_controller = ProcessController(user=user)

    process = await process_controller.create_process(
        name=name,
        description=description,
        is_active=is_active,
    )

    return ProcessPayloadType.to_result(process=process)

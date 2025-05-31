from typing import Optional

from src.api.management.graphql.types.schemas_type.process_type import ProcessType
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.auth_decorators import login_required


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
):
    # Get data by `User`
    user_obj: User = info.context['user']

    process_controller = ProcessController(user=user_obj)

    process_obj = None

    if id:
        process_obj = await process_controller.get_process_by_id(id=id)
    elif name:
        process_obj = await process_controller.get_process_by_name(name=name)

    return ProcessType().to_result(process=process_obj)

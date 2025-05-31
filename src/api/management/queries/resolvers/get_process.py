from typing import Optional

from src.api.management.graphql.types.schemas_type.process_type import ProcessType
from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.auth_decorators import login_required
from src.utils.exceptions import EmptyDataException


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

    process_obj = await process_controller.get_process_by_id(id=id)
    if process_obj is None:
        process_obj = await process_controller.get_process_by_name(name=name)

    if not process_obj:
        raise EmptyDataException(message='<error?>')

    return ProcessType().to_result(process=process_obj)

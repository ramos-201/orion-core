from src.controllers.process_controller import ProcessController
from src.models import User
from src.utils.login_required import login_required
from src.utils.validate_data import validate_not_empty_fields


delete_process_type_gql = """
deleteProcess(
    id: String!
): Boolean
"""


@login_required
async def resolve_delete_process(
    _, info,
    id: str,
) -> bool:
    validate_not_empty_fields(id=id)

    # Get data by `User`
    user: User = info.context['user']

    process_controller = ProcessController(user=user)

    ok = await process_controller.delete_process(process_id=id)

    return ok

from src.api.resolvers.payload import process_to_dict
from src.constants import STR_OR_NONE
from src.controllers.process_controller import ProcessController
from src.utils.auth_decorators import login_required


@login_required
async def resolve_process(
        _, info,
        id: STR_OR_NONE = None,
        name: STR_OR_NONE = None,
):
    user = info.context.get('user')

    process_controller = ProcessController()
    process = await process_controller.get_process_by_unique_key(user_id=user.id, id=id, name=name)

    return process_to_dict(process=process)

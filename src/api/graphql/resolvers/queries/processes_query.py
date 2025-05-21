from src.api.graphql.payload import process_to_dict
from src.controllers.process_controller import ProcessController
from src.utils.auth_decorators import login_required
from src.utils.constants import (
    DICT_OR_NONE,
    STR_OR_NONE,
)


@login_required
async def resolve_process(
        _, info,
        id: STR_OR_NONE = None,
        name: STR_OR_NONE = None,
) -> DICT_OR_NONE:
    # Get data by `User`
    user = info.context.get('user')

    process_controller = ProcessController()
    process = await process_controller.get_process_by_unique_key(user_id=user.id, id=id, name=name)

    return process_to_dict(process=process)

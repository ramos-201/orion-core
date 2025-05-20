from src.api.resolvers.payload import process_to_dict
from src.controllers.process_controller import ProcessController
from src.utils.auth_decorators import login_required


@login_required
async def resolve_process(
        _, info,
        id: str,
):
    process_controller = ProcessController()
    process = await process_controller.get_process_by_id(id=id)

    return process_to_dict(process=process)

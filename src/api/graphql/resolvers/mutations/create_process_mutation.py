from src.api.graphql.payload import process_to_dict
from src.controllers.process_controller import ProcessController
from src.utils.auth_decorators import login_required
from src.utils.constants import STR_OR_NONE
from src.utils.validate_data import validate_required_data


@login_required
async def resolve_create_process(
    _, info,
    name: str,
    description: STR_OR_NONE = None,
) -> dict:
    validate_required_data(name=name)

    process_controller = ProcessController()
    process = await process_controller.create_process(
        name=name,
        description=description,
        user=info.context['user'],
    )

    return {'process': process_to_dict(process=process)}

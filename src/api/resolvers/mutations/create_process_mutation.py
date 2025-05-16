from src.api.resolvers.payload import process_to_dict
from src.constants import STR_OR_NONE
from src.controllers.process_controller import ProcessController
from src.utils.validate_data import validate_required_data


async def resolve_create_process(
    _, info,
    name: str,
    description: STR_OR_NONE = None,
):
    validate_required_data(name=name)

    process_controller = ProcessController()
    process = await process_controller.create_process(
        name=name,
        description=description,
    )

    return {'process': process_to_dict(process=process)}

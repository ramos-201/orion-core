from src.api.resolvers.payload import process_to_dict
from src.controllers.process_controller import ProcessController


async def resolve_create_process(
        _, info,
        name: str,
        description: str,
):
    process_controller = ProcessController()
    process = await process_controller.create_process(
        name=name,
        description=description,
    )
    return {'process': process_to_dict(process=process)}

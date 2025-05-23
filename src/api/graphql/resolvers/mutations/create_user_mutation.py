from src.api.graphql.payload import user_to_dict
from src.controllers.user_controller import UserController
from src.utils.validate_data import validate_required_data


async def resolve_create_user(
    _, info,
    name: str,
    last_name: str,
    username: str,
    email: str,
    mobile_phone: str,
    password: str,
) -> dict:
    validate_required_data(
        name=name,
        last_name=last_name,
        username=username,
        email=email,
        mobile_phone=mobile_phone,
        password=password,
    )

    user_controller = UserController()
    user_created = await user_controller.create_user(
        name=name,
        last_name=last_name,
        username=username,
        email=email,
        mobile_phone=mobile_phone,
        password=password,
    )

    return {'user': user_to_dict(user=user_created)}

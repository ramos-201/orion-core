from typing import (
    Any,
    Optional,
)

from src.api.gql.user.types.schemes_type.user_type import UserType
from src.controllers.utils.instance_helper import InstanceHelper
from src.models import User
from src.utils.login_required import login_required


update_user_type_gql = """
updateUser(
    name: String
    lastName: String
    mobilePhone: String
): UserType
"""


@login_required
async def resolve_update_user(
    _, info,
    name: Optional[str] = None,
    last_name: Optional[str] = None,
    mobile_phone: Optional[str] = None,
) -> dict[str, Any]:
    # Get data by `User`
    user: User = info.context['user']

    fields_to_update = {
        'name': name,
        'last_name': last_name,
        'mobile_phone': mobile_phone,
    }
    instance_helper = InstanceHelper(instance=user)
    instance_helper.apply_updates(fields=fields_to_update)
    await instance_helper.save_instance()

    return UserType.to_result(user=user)

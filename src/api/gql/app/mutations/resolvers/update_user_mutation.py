from typing import (
    Any,
    Optional,
)

from src.api.gql.user.types.schemes_type.user_type import UserType
from src.controllers.base_controller import (
    apply_valid_updates_or_fail,
    safe_save,
)
from src.models import User
from src.utils.format_date import get_current_datetime
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
    apply_valid_updates_or_fail(fields_to_update, user)

    user.modified_at = get_current_datetime()
    await safe_save(instance=user)

    return UserType.to_result(user=user)

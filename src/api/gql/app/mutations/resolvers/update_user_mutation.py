from typing import (
    Any,
    Optional,
)

from tortoise.exceptions import IntegrityError

from src.api.gql.user.types.schemes_type.user_type import UserType
from src.models import User
from src.utils.exceptions import (
    DuplicateFieldException,
    EmptyDataException,
)
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
    if not any([name, last_name, mobile_phone]):
        raise EmptyDataException(message='There is no data to update.')

    # Get data by `User`
    user: User = info.context['user']

    user.name = name or user.name
    user.last_name = last_name or user.last_name
    user.mobile_phone = mobile_phone or user.mobile_phone

    try:
        await user.save()
    except IntegrityError:
        raise DuplicateFieldException(message='The data for the field "mobile_phone" already exists.')

    return UserType.to_result(user=user)

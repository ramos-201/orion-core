from typing import (
    Any,
    Optional,
)

from src.api.gql.user.types.schemes_type.user_type import UserType
from src.models import User
from src.utils.login_required import login_required


get_user_type_gql = """
getUser: UserType
"""


@login_required
async def resolve_get_user(_, info) -> Optional[dict[str, Any]]:
    # Get data by `User`
    user: User = info.context['user']

    return UserType().to_result(user=user)

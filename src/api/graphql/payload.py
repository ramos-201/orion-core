from typing import Optional

from src.models import (
    Process,
    User,
)
from src.utils.constants import DICT_OR_NONE


def user_to_dict(user: User) -> DICT_OR_NONE:
    if not user:
        return None
    return {
        'id': str(user.id),
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'mobile_phone': user.mobile_phone,
    }


def process_to_dict(process: Optional[Process]) -> DICT_OR_NONE:
    if not process:
        return None
    return {
        'id': str(process.id),
        'created_at': process.created_at,
        'modified_at': process.modified_at,
        'name': process.name,
        'description': process.description,
    }

from typing import Any

from src.enums.error_type_enum import ErrorTypeEnum


class DuplicateFieldException(Exception):
    def __init__(self, message: str, **details: Any):
        self.message = message
        self.error_type = ErrorTypeEnum.DUPLICATE_FIELD_ERROR.value
        if details:
            self.details = details

from typing import Any

from src.enums.error_type_enum import ErrorTypeEnum


class ExceptionBase(Exception):
    def __init__(self, message: str, error_type: ErrorTypeEnum, **details: Any):
        self.message = message
        self.error_type = error_type.value
        self.details = details


class DuplicateFieldException(ExceptionBase):
    def __init__(self, message: str, **details: Any):
        super().__init__(
            message=message,
            error_type=ErrorTypeEnum.DUPLICATE_FIELD_ERROR,
            **details,
        )


class EmptyDataException(ExceptionBase):
    def __init__(self, message: str, **details: Any):
        super().__init__(
            message=message,
            error_type=ErrorTypeEnum.EMPTY_DATA_ERROR,
            **details,
        )

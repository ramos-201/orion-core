from src.utils.enums.type_error import ErrorTypeEnum


class GeneralException(Exception):
    def __init__(self, message: str, error_type: ErrorTypeEnum):
        self.message = message
        self.error_type = error_type.value


class EmptyDataException(GeneralException):
    def __init__(self, message: str):
        super().__init__(message=message, error_type=ErrorTypeEnum.EMPTY_DATA_ERROR)


class DuplicateFieldException(GeneralException):
    def __init__(self, message: str):
        super().__init__(message=message, error_type=ErrorTypeEnum.DUPLICATE_FIELD_ERROR)

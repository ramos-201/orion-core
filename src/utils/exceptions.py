from src.utils.constants import ErrorTypeEnum


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


class InvalidCredentialException(GeneralException):
    def __init__(self, message: str):
        super().__init__(message=message, error_type=ErrorTypeEnum.INVALID_CREDENTIALS_ERROR)


class UnauthorizedException(GeneralException):
    def __init__(self, message: str):
        super().__init__(message=message, error_type=ErrorTypeEnum.UNAUTHORIZED_ERROR)


class UnknownError(GeneralException):
    def __init__(self, message: str):
        super().__init__(message=message, error_type=ErrorTypeEnum.UNKNOWN_ERROR)

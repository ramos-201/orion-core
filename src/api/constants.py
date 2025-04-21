from enum import Enum


ENDPOINT_NAME = '/graphql'


class ErrorTypeEnum(Enum):
    EMPTY_DATA_ERROR = 'EMPTY_DATA_ERROR'
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    INTERNAL_ERROR = 'INTERNAL_ERROR'

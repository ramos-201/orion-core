from src.utils.constants import ErrorTypeEnum
from src.utils.exceptions import GraphQLException


def validate_required_data(**kwargs) -> None:
    missing_fields = [key for key, value in kwargs.items() if value == '']
    if missing_fields:
        raise GraphQLException(
            message=f'The following fields cannot be empty: {missing_fields}.',
            error_type=ErrorTypeEnum.EMPTY_DATA_ERROR,
        )

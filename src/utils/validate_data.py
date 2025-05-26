from src.utils.exceptions import EmptyDataException


def validate_not_empty_fields(**kwargs: str) -> None:
    missing_fields = [key for key, value in kwargs.items() if value == '']
    if missing_fields:
        raise EmptyDataException(message=f'The following fields cannot be empty: {missing_fields}.')

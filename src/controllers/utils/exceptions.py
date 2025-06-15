from src.utils.exceptions import EmptyDataException


class EmptyDataNotExistIdException(EmptyDataException):
    def __init__(self, id: str):
        super().__init__(message=f'The process for the id: "{id}" does not exist.')

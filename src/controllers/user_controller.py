from tortoise.exceptions import IntegrityError

from src.exceptions import DuplicateFieldError
from src.models.user import User


class UserController:
    def __init__(self):
        self.user = User

    async def create_user(
            self,
            name,
            last_name,
            username,
            email,
            mobile_phone,
            password,
    ):
        try:
            return await self.user.create(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldError(message=f'The data for the field "{field_name}" already exists.')

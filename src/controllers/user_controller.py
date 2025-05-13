from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from src.exceptions import DuplicateFieldError
from src.models.user import User


class UserController:
    def __init__(self):
        self.model = User

    async def create_user(
            self,
            name,
            last_name,
            username,
            email,
            mobile_phone,
            password,
    ) -> 'User':
        try:
            return await self.model.create(
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

    async def get_user_by_credentials(self, user, password) -> 'User':
        return await self.model.get_or_none(
            Q(email=user) | Q(username=user),
            password=password,
        )

    def get_dict(self, user):
        return user.__dict__()

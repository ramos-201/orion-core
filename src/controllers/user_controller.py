from tortoise.expressions import Q

from src.controllers.base_controller import BaseController
from src.models.user import User


class UserController(BaseController):
    def __init__(self):
        super().__init__(model=User)

    async def create_user(
        self,
        name: str,
        last_name: str,
        username: str,
        email: str,
        mobile_phone: str,
        password: str,
    ) -> 'User':
        return await self._create(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
        )

    async def get_user_by_credentials(
        self,
        user,
        password,
    ) -> 'User':
        return await self._get_or_none(
            Q(email=user) |
            Q(username=user),
            password=password,
        )

    async def get_user_by_id(self, user_id):
        return await self._get_or_none(id=user_id)

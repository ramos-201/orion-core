from typing import Optional

from tortoise.expressions import Q

from src.controllers.base_controller import BaseController
from src.models import User


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
    ) -> User:
        is_account_active = True

        return await self._create(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
            is_account_active=is_account_active,
        )

    async def get_user_by_credentials(
            self,
            identifier: str,
            password: str,
    ) -> Optional[User]:
        return await self._get_or_none(
            Q(email=identifier) | Q(username=identifier),
            password=password,
        )

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self._get_by_id(id=user_id)

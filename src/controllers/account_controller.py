from tortoise.expressions import Q

from src.controllers.base_controller import BaseController
from src.models import Account


class AccountController(BaseController):
    def __init__(self):
        super().__init__(model=Account)

    async def create_account(
        self,
        email: str,
        username: str,
        password: str,
    ) -> Account:
        return await self._create(
            email=email,
            username=username,
            password=password,
        )

    async def get_account_by_credentials(
        self,
        identifier: str,
        password: str,
    ) -> Account:
        return await self._get_or_none(
            Q(email=identifier) | Q(username=identifier),
            password=password,
        )

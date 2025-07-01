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

    async def get_account(
        self,
        user: str,
        password: str,
    ):
        return await self.model.get_or_none(username=user, password=password)

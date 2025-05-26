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
    ):
        return await self._create(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
            is_account_active=True,
        )

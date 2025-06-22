from src.models import Account


class AccountController:
    def __init__(self):
        self.model = Account()

    async def create_account(
        self,
        email: str,
        username: str,
        password: str,
    ) -> Account:
        return await self.model.create(
            email=email,
            username=username,
            password=password,
        )

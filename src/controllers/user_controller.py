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
        return await self.user.create(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
        )

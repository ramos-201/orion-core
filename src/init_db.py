from tortoise import Tortoise

from configs import (
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_URL,
    DB_USER,
    IS_DEV,
)


async def init_db() -> None:
    await Tortoise.init(
        db_url=f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}',
        modules={'models': ['src.models']},
    )
    if IS_DEV:
        await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()

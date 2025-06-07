from starlette.applications import Starlette

from src.api.router_api import router
from src.db_config import (
    close_db,
    initialize_db,
)


app = Starlette(
    routes=router,
    on_startup=[initialize_db],
    on_shutdown=[close_db],
)

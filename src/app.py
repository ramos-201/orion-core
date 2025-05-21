from starlette.applications import Starlette

from src.api.graphql.router import router_gql
from src.init_db import (
    close_db,
    init_db,
)


app = Starlette(
    routes=router_gql,
    on_startup=[init_db],
    on_shutdown=[close_db],
)

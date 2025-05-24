from starlette.applications import Starlette

from src.api.router.router_gql import router


app = Starlette(routes=router)

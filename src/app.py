from starlette.applications import Starlette

from src.api.router import routes


app = Starlette(routes=routes)

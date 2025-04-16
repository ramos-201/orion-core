from ariadne import make_executable_schema

from src.api.resolvers.mutations import mutation
from src.api.resolvers.queries import query
from src.api.resolvers.types import (
    auth_payload_type,
    user_type,
)
from src.api.typedefs import type_defs


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    user_type,
    auth_payload_type,
    convert_names_case=True,
)

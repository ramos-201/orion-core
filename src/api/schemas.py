from ariadne import make_executable_schema

from src.api.resolvers.mutations import mutation
from src.api.resolvers.queries import query
from src.api.typedefs import type_defs


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    convert_names_case=True,
)

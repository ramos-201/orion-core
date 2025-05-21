from ariadne import make_executable_schema

from src.api.graphql.resolvers.mutations import mutation
from src.api.graphql.resolvers.queries import query
from src.api.graphql.typedefs import type_defs


schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    convert_names_case=True,
)

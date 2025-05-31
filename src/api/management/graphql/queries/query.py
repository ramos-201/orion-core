from ariadne import QueryType

from src.api.management.graphql.queries.resolvers.get_process import resolve_get_process


query = QueryType()

query.set_field('getProcess', resolve_get_process)

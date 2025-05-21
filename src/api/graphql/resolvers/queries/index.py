from ariadne import QueryType

from src.api.graphql.resolvers.queries.processes_query import resolve_process


query = QueryType()


query.set_field('process', resolve_process)

from ariadne import QueryType

from src.api.gql.app.queries.resolvers.get_process_query import (
    resolve_get_process,
)
from src.api.gql.app.queries.resolvers.get_processes_query import (
    resolve_get_processes,
)
from src.api.gql.app.queries.resolvers.get_user_query import resolve_get_user


query = QueryType()

query.set_field('getProcess', resolve_get_process)
query.set_field('getProcesses', resolve_get_processes)
query.set_field('getUser', resolve_get_user)

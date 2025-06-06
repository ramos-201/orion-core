from ariadne import QueryType

from src.api.gql.app.queries.resolvers.get_process_query import (
    resolve_get_process,
)
from src.api.gql.app.queries.resolvers.get_processes_query import (
    resolve_get_processes,
)


app_query = QueryType()

app_query.set_field('getProcess', resolve_get_process)
app_query.set_field('getProcesses', resolve_get_processes)

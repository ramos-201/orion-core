from ariadne import gql

from src.api.gql.app.mutations.resolvers.delete_process_mutation import (
    delete_process_type_gql,
)
from src.api.gql.app.mutations.resolvers.register_process_mutation import (
    register_process_type_gql,
)
from src.api.gql.app.mutations.resolvers.update_process_mutation import (
    update_process_type_gql,
)
from src.api.gql.app.mutations.resolvers.update_user_mutation import (
    update_user_type_gql,
)
from src.api.gql.app.queries.resolvers.get_process_query import (
    get_process_type_gql,
)
from src.api.gql.app.queries.resolvers.get_processes_query import (
    get_processes_type_gql,
)
from src.api.gql.app.queries.resolvers.get_user_query import get_user_type_gql
from src.api.gql.app.types.payloads.process_payload_type import (
    ProcessPayloadType,
)
from src.api.gql.app.types.payloads.processes_payload_type import (
    ProcessesPayloadType,
)
from src.api.gql.app.types.schemes_type.process_type import ProcessType
from src.api.gql.user.types.schemes_type.user_type import UserType


_schema_type_def = '\n'.join([
    UserType.type_def_gql.strip(),
    ProcessType.type_def_gql.strip(),
])

_payload_type_def = '\n'.join([
    ProcessPayloadType.type_def_gql.strip(),
    ProcessesPayloadType.type_def_gql.strip(),
])

_query_type_def = f"""
type Query {{
    {get_process_type_gql.strip()}
    {get_processes_type_gql.strip()}
    {get_user_type_gql.strip()}
}}
"""

_mutation_type_def = f"""
type Mutation {{
    {register_process_type_gql.strip()}
    {update_user_type_gql.strip()}
    {update_process_type_gql.strip()}
    {delete_process_type_gql.strip()}
}}
"""

typedefs = gql(_query_type_def + _mutation_type_def + _schema_type_def + _payload_type_def)

__all__ = ['typedefs']

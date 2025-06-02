from ariadne import gql

from src.api.management.graphql.mutations.resolvers.login_mutation import login_type_gql
from src.api.management.graphql.mutations.resolvers.register_process_mutation import (
    register_process_type_gql,
)
from src.api.management.graphql.mutations.resolvers.register_user_mutation import (
    register_user_type_gql,
)
from src.api.management.graphql.queries.resolvers.get_process_query import (
    get_process_type_gql,
)
from src.api.management.graphql.queries.resolvers.get_processes_query import (
    get_processes_type_gql,
)
from src.api.management.graphql.types.payloads.process_payload_type import (
    ProcessPayloadType,
)
from src.api.management.graphql.types.payloads.processes_payload_type import (
    ProcessesPayloadType,
)
from src.api.management.graphql.types.payloads.user_payload_type import UserPayloadType
from src.api.management.graphql.types.schemas_type.process_type import ProcessType
from src.api.management.graphql.types.schemas_type.user_type import UserType


schema_type_def = '\n'.join([
    UserType.type_def_gql.strip(),
    ProcessType.type_def_gql.strip(),
])

payload_type_def = '\n'.join([
    UserPayloadType.type_def_gql.strip(),
    ProcessPayloadType.type_def_gql.strip(),
    ProcessesPayloadType.type_def_gql.strip(),
])

query_type_def = f"""
type Query {{
    {get_process_type_gql.strip()}
    {get_processes_type_gql.strip()}
}}
"""

mutation_type_def = f"""
type Mutation {{
    {register_user_type_gql.strip()}
    {login_type_gql.strip()}
    {register_process_type_gql.strip()}
}}
"""

type_defs = gql(query_type_def + mutation_type_def + schema_type_def + payload_type_def)

__all__ = ['type_defs']

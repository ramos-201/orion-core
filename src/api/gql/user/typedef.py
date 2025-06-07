from ariadne import gql

from src.api.gql.user.mutations.resolvers.login_mutation import login_type_gql
from src.api.gql.user.mutations.resolvers.register_user_mutation import (
    register_user_type_gql,
)
from src.api.gql.user.types.payloads.user_payload_type import UserPayloadType
from src.api.gql.user.types.schemes_type.user_type import UserType


_schema_type_def = '\n'.join([
    UserType.type_def_gql.strip(),
])

_payload_type_def = '\n'.join([
    UserPayloadType.type_def_gql.strip(),
])

_query_type_def = """
type Query {
    _empty: String
}
"""

_mutation_type_def = f"""
type Mutation {{
    {register_user_type_gql.strip()}
    {login_type_gql.strip()}
}}
"""

typedefs = gql(_query_type_def + _mutation_type_def + _schema_type_def + _payload_type_def)

__all__ = ['typedefs']

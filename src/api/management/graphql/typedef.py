from ariadne import gql

from src.api.management.graphql.mutations.resolvers.register_user_mutation import (
    register_user_type_gql,
)
from src.api.management.graphql.types.payloads.user_payload_type import UserPayloadType
from src.api.management.graphql.types.schemas_type.user_type import UserType


schema_type_def = UserType.type_def_gql.strip()

payload_type_def = UserPayloadType.type_def_gql.strip()

query_type_def = '''
type Query {
    _empty: String!
}
'''

mutation_type_def = f'''
type Mutation {{
    {register_user_type_gql.strip()}
}}
'''

type_defs = gql(query_type_def + mutation_type_def + schema_type_def + payload_type_def)

__all__ = ['type_defs']

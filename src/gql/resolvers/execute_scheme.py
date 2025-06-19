from ariadne import graphql

from src.gql.resolvers.auth.schema import schema


async def execute_gql(data):
    return await graphql(
        schema,
        data,
        context_value={},
    )

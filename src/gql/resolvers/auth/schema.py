from ariadne_graphql_modules import make_executable_schema

from src.gql.resolvers.auth.mutations import CreateUserMutation
from src.gql.resolvers.auth.queries import EmptyQuery


schema = make_executable_schema(EmptyQuery, CreateUserMutation)

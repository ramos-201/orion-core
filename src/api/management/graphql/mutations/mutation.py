from ariadne import MutationType

from src.api.management.graphql.mutations.resolvers.register_user import (
    resolve_register_user,
)


mutation_gql = MutationType()

mutation_gql.set_field('registerUser', resolve_register_user)

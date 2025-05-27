from ariadne import MutationType

from src.api.management.graphql.mutations.resolvers.login_mutation import resolve_login
from src.api.management.graphql.mutations.resolvers.register_user_mutation import (
    resolve_register_user,
)


mutation = MutationType()

mutation.set_field('registerUser', resolve_register_user)
mutation.set_field('login', resolve_login)

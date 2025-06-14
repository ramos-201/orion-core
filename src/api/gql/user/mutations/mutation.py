from ariadne import MutationType

from src.api.gql.user.mutations.resolvers.login_mutation import resolve_login
from src.api.gql.user.mutations.resolvers.register_user_mutation import (
    resolve_register_user,
)


mutation = MutationType()

mutation.set_field('registerUser', resolve_register_user)
mutation.set_field('login', resolve_login)

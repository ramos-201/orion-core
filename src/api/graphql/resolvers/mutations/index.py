from ariadne import MutationType

from src.api.graphql.resolvers.mutations.create_process_mutation import (
    resolve_create_process,
)
from src.api.graphql.resolvers.mutations.create_user_mutation import resolve_create_user
from src.api.graphql.resolvers.mutations.login_mutation import resolve_login


mutation = MutationType()

mutation.set_field('createUser', resolve_create_user)
mutation.set_field('login', resolve_login)
mutation.set_field('createProcess', resolve_create_process)

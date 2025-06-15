from ariadne import MutationType

from src.api.gql.app.mutations.resolvers.delete_process_mutation import (
    resolve_delete_process,
)
from src.api.gql.app.mutations.resolvers.register_process_mutation import (
    resolve_register_process,
)
from src.api.gql.app.mutations.resolvers.update_process_mutation import (
    resolve_update_process,
)
from src.api.gql.app.mutations.resolvers.update_user_mutation import resolve_update_user


mutation = MutationType()


mutation.set_field('registerProcess', resolve_register_process)
mutation.set_field('updateUser', resolve_update_user)
mutation.set_field('updateProcess', resolve_update_process)
mutation.set_field('deleteProcess', resolve_delete_process)

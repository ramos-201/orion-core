from ariadne import MutationType

from src.api.gql.app.mutations.resolvers.register_process_mutation import (
    resolve_register_process,
)


mutation = MutationType()


mutation.set_field('registerProcess', resolve_register_process)

from src.api.gql.utils.graphql_type_abs import GraphQLTypeAbs
from src.models.process import Process


class ProcessType(GraphQLTypeAbs):
    type_def_gql = """
    type ProcessType {
        id: String!
        name: String!
        description: String
        isActive: Boolean!
        createdAt: String!
        modifiedAt: String!
    }
    """

    @classmethod
    def to_result(cls, process: Process) -> dict[str, str]:
        return {
            'id': process.id,
            'name': process.name,
            'description': process.description,
            'is_active': process.is_active,
            'created_at': process.created_at,
            'modified_at': process.modified_at,
        }

from api.schema import schema
from strawberry.asgi import GraphQL as BaseGraphQL


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

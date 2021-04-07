from strawberry.asgi import GraphQL as BaseGraphQL

from .schema import schema


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

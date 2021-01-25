import typing

from api.context import Context
from api.schema import schema
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

    async def get_context(self, request: typing.Union[Request, WebSocket]) -> Context:
        return Context(request=request, session=request.state.session)

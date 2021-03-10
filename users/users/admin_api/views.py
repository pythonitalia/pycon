import typing

from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL

from users.admin_api.context import Context
from users.admin_api.schema import schema


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

    async def get_context(self, request: typing.Union[Request, WebSocket]) -> Context:
        return Context(request=request, session=request.state.session)

from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.utils.debug import pretty_print_graphql_operation

from users.internal_api.context import Context
from users.internal_api.schema import schema


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

    async def get_context(
        self, request: Union[Request, WebSocket], response: Optional[Response]
    ) -> Context:
        return Context(request=request, session=request.state.session)

    async def handle_websocket(self, scope: Scope, receive: Receive, send: Send):
        websocket = WebSocket(scope=scope, receive=receive, send=send)
        await websocket.close()

    async def execute(
        self, query, variables=None, context=None, operation_name=None, root_value=None
    ):
        if self.debug:
            pretty_print_graphql_operation(operation_name, query, variables)

        return await self.schema.execute(
            query,
            root_value=root_value,
            variable_values=variables,
            operation_name=operation_name,
            context_value=context,
            validate_queries=False,
        )

from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL

from users.admin_api.context import Context
from users.admin_api.schema import schema
from users.settings import PASTAPORTO_ACTION_SECRET, PASTAPORTO_ACTION_X_HEADER


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

    async def handle_http(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        root_value = await self.get_root_value(request)
        context = await self.get_context(request)

        response = await self.get_http_response(
            request=request,
            execute=self.execute,
            process_result=self.process_result,
            graphiql=self.graphiql,
            root_value=root_value,
            context=context,
        )

        if context.pastaporto_action:
            response.headers[
                PASTAPORTO_ACTION_X_HEADER
            ] = context.pastaporto_action.sign(PASTAPORTO_ACTION_SECRET)

        await response(scope, receive, send)

    async def get_context(
        self, request: Union[Request, WebSocket], response: Optional[Response] = None
    ) -> Context:
        return Context(request=request, session=request.state.session)

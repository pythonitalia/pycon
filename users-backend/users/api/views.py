from typing import Optional, Union

from pythonit_toolkit.headers import PASTAPORTO_ACTION_X_HEADER
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.asgi.handlers.http_handler import HTTPHandler

from users.api.context import Context
from users.api.schema import schema
from users.settings import PASTAPORTO_ACTION_SECRET


class CustomHTTPHandler(HTTPHandler):
    async def handle(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        root_value = await self.get_root_value(request)

        sub_response = Response(
            content=None,
            status_code=None,  # type: ignore
            headers=None,
            media_type=None,
            background=None,
        )

        context = await self.get_context(request=request, response=sub_response)

        response = await self.get_http_response(
            request=request,
            execute=self.execute,
            process_result=self.process_result,
            graphiql=self.graphiql,
            root_value=root_value,
            context=context,
        )

        response.headers.raw.extend(sub_response.headers.raw)

        if sub_response.background:
            response.background = sub_response.background

        if sub_response.status_code:
            response.status_code = sub_response.status_code

        if context.pastaporto_action:
            response.headers[
                PASTAPORTO_ACTION_X_HEADER
            ] = context.pastaporto_action.sign(PASTAPORTO_ACTION_SECRET)

        await response(scope, receive, send)


class GraphQL(BaseGraphQL):
    http_handler_class = CustomHTTPHandler

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(schema, *args, **kwargs)

    async def get_context(
        self, request: Union[Request, WebSocket], response: Optional[Response] = None
    ) -> Context:
        return Context(request=request, session=request.state.session)

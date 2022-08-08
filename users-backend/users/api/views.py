from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.asgi.handlers.http_handler import HTTPHandler

from users.api.context import Context
from users.api.schema import schema
from users.settings import ENVIRONMENT, IDENTITY_COOKIE_KEY


class CustomHTTPHandler(HTTPHandler):
    async def handle(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        root_value = await self.get_root_value(request)

        sub_response = Response()
        sub_response.status_code = None  # type: ignore
        del sub_response.headers["content-length"]

        context = await self.get_context(request=request, response=sub_response)

        response = await self.get_http_response(
            request=request,
            execute=self.execute,
            process_result=self.process_result,
            root_value=root_value,
            context=context,
        )

        response.headers.raw.extend(sub_response.headers.raw)

        if sub_response.background:
            response.background = sub_response.background

        if sub_response.status_code:
            response.status_code = sub_response.status_code

        if context._authenticated_as:
            response.set_cookie(
                key=IDENTITY_COOKIE_KEY,
                value=context._authenticated_as.create_identity_token(),
                expires=60 * 60 * 24 * 90,
                httponly=True,
                secure=ENVIRONMENT != "local",
                samesite="strict",
            )

        await response(scope, receive, send)


class GraphQL(BaseGraphQL):
    http_handler_class = CustomHTTPHandler

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(schema, *args, **kwargs)

    async def get_context(
        self, request: Union[Request, WebSocket], response: Optional[Response] = None
    ) -> Context:
        return Context(
            request=request, response=response, session=request.state.session
        )

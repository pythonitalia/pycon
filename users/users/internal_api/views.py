import typing

from starlette.requests import Request
from starlette.types import Receive, Scope, Send
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL
from strawberry.asgi.http import get_http_response
from strawberry.utils.debug import pretty_print_graphql_operation

from users.internal_api.context import Context
from users.internal_api.permissions import is_service
from users.internal_api.schema import schema


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

    async def get_context(self, request: typing.Union[Request, WebSocket]) -> Context:
        return Context(request=request, session=request.state.session)

    async def handle_http(self, scope: Scope, receive: Receive, send: Send):
        request = Request(scope=scope, receive=receive)
        root_value = await self.get_root_value(request)
        context = await self.get_context(request)

        if not is_service(request):
            raise ValueError("Unauthorized")

        response = await get_http_response(
            request=request,
            execute=self.execute,
            process_result=self.process_result,
            graphiql=self.graphiql,
            root_value=root_value,
            context=context,
        )

        await response(scope, receive, send)

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

import logging
from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.asgi import GraphQL as BaseGraphQL

from association.api.context import Context
from association.api.schema import schema

logger = logging.getLogger(__name__)


class GraphQL(BaseGraphQL):
    def __init__(self) -> None:
        super().__init__(schema)

    async def get_context(
        self, request: Union[Request, WebSocket], response: Optional[Response] = None
    ) -> Context:
        return Context(request=request, session=request.state.session)

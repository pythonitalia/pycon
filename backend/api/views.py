from typing import Any

from django.http.request import HttpRequest
from strawberry.django.views import AsyncGraphQLView as BaseGraphQLVew

from api.context import Context


class GraphQLView(BaseGraphQLVew):
    async def get_context(self, request: HttpRequest, response: Any) -> Context:
        return Context(request=request, response=response)

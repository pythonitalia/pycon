from typing import Any

from django.http import HttpResponse
from django.http.request import HttpRequest
from strawberry.django.views import GraphQLView as BaseGraphQLVew

from api.context import Context


class GraphQLView(BaseGraphQLVew):
    def get_context(self, request: HttpRequest, response: Any) -> Context:
        return Context(request=request, response=response)


def health_check(request):
    return HttpResponse(status=200)

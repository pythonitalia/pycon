from api.context import Context
from django.http.request import HttpRequest

from strawberry.django.views import GraphQLView as BaseGraphQLVew


class GraphQLView(BaseGraphQLVew):
    def get_context(self, request: HttpRequest) -> Context:
        return Context(request=request)

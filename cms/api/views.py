from django.http import HttpRequest, HttpResponse
from strawberry.django.views import GraphQLView as BaseGraphQLView


class GraphQLView(BaseGraphQLView):
    def get_context(self, request: HttpRequest, response: HttpResponse) -> dict:
        return {
            "request": request,
        }

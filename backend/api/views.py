import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.views.generic import View
from graphql import graphql_sync
from graphql.error import format_error as format_graphql_error

from .schema import schema


class GraphQLView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            return render(request, "api/graphiql.html")

        if request.method != "POST":
            return HttpResponseNotAllowed(["GET", "POST"])

        query, variables = self.parse_body(request)

        response = graphql_sync(
            schema, query, variable_values=variables, context_value=request
        )

        response_data = {"data": response.data}

        if response.errors:
            response_data["errors"] = [
                format_graphql_error(err) for err in response.errors
            ]

        status_code = 400 if response.errors else 200
        return JsonResponse(response_data, status=status_code)

    def parse_body(self, request):
        body = json.loads(request.body)
        return body.get("query", ""), body.get("variables", {})

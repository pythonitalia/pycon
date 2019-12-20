import json
import logging

from django.http import HttpResponseNotAllowed, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from graphql import graphql_sync
from graphql.error import format_error as format_graphql_error
from strawberry.django.views import GraphQLView


class CustomGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):

        if request.method.lower() not in ("get", "post"):
            return HttpResponseNotAllowed(
                ["GET", "POST"], "GraphQL only supports GET and POST requests."
            )

        if "text/html" in request.META.get("HTTP_ACCEPT", ""):
            return render(
                request,
                "graphql/playground.html",
                {"REQUEST_PATH": request.get_full_path()},
            )

        data = json.loads(request.body)

        try:
            query = data["query"]
            variables = data.get("variables")
            operation_name = data.get("operationName")
        except KeyError:
            return HttpResponseBadRequest("No GraphQL query found in the request")

        context = {"request": request}

        result = graphql_sync(
            self.schema,
            query,
            variable_values=variables,
            context_value=context,
            operation_name=operation_name,
        )

        response_data = {"data": result.data}

        if result.errors:
            response_data["errors"] = [
                format_graphql_error(err) for err in result.errors
            ]
            self._capture_sentry_exceptions(result.errors)

        return JsonResponse(response_data, status=200)

    def _capture_sentry_exceptions(self, errors):
        for error in errors:
            if hasattr(error, "original_error"):
                logging.error(error.original_error)
            else:
                logging.error(error, exc_info=True)

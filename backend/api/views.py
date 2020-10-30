import json
import logging
import os

import strawberry
from django.http import HttpResponseNotAllowed, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.template import RequestContext, Template
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
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
            return self._render_graphiql(request)

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

    def _render_graphiql(self, request, context=None):
        try:
            template = Template(render_to_string("graphql/graphiql.html"))
        except TemplateDoesNotExist:
            template = Template(
                open(
                    os.path.join(
                        os.path.dirname(os.path.abspath(strawberry.__file__)),
                        "static/graphiql.html",
                    ),
                    "r",
                ).read()
            )

        context = context or {}
        context.update({"SUBSCRIPTION_ENABLED": "false"})

        response = TemplateResponse(request=request, template=None, context=context)
        response.content = template.render(RequestContext(request, context))

        return response

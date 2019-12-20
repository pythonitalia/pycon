import json
import logging

import sentry_sdk
from strawberry.contrib.django.views import GraphQLView


class CustomGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        resp = super(CustomGraphQLView, self).dispatch(request, *args, **kwargs)
        errors = json.loads(resp.getvalue()).get("errors", [])
        if errors:
            self._capture_sentry_exceptions(errors)
        return resp

    def _capture_sentry_exceptions(self, errors):
        for error in errors:
            logging.error(error, exc_info=True)
            sentry_sdk.capture_exception(error["message"])

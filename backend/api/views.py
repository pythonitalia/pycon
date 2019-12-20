import json
import logging

from strawberry.contrib.django.views import GraphQLView


class CustomGraphQLView(GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        resp = super(CustomGraphQLView, self).dispatch(request, *args, **kwargs)
        if resp.status_code == 400:
            logging.error(json.loads(resp.getvalue())["errors"], exc_info=True)
            return resp
        return resp

from starlette.applications import Starlette
from starlette.routing import Route

from association.api.views import GraphQL
from association.webhooks.views import stripe_webhook

app = Starlette(
    debug=True,
    routes=[
        Route("/graphql", GraphQL()),
        Route("/stripe-webhook", endpoint=stripe_webhook, methods=["POST"]),
    ],
)

import logging

from pythonit_toolkit.starlette_backend.middleware import pastaporto_auth_middleware
from starlette.applications import Starlette
from starlette.routing import Route

from api.views import GraphQL
from association.settings import DEBUG, PASTAPORTO_SECRET
from association.stripe import views as stripe_views
from association.webhooks.views import stripe_webhook
from database.db import database

logging.basicConfig(level=logging.INFO)


app = Starlette(
    debug=DEBUG,
    routes=[
        Route("/graphql", GraphQL()),
        Route("/stripe-webhook", stripe_webhook, methods=["POST"]),
        # TODO DELETE THESE URLS
        Route("/stripe/do-payment", stripe_views.PaymentView),
    ],
    middleware=[
        pastaporto_auth_middleware(PASTAPORTO_SECRET),
    ],
)


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

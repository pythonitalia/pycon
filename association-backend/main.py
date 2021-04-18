import logging

from pythonit_toolkit.starlette_backend.middleware import pastaporto_auth_middleware
from starlette.applications import Starlette
from starlette.routing import Route

from src.api.views import GraphQL
from src.association.settings import DEBUG, PASTAPORTO_SECRET
from src.database.db import database
from src.webhooks.views import stripe_webhook

logging.basicConfig(level=logging.INFO)


app = Starlette(
    debug=DEBUG,
    routes=[
        Route("/graphql", GraphQL()),
        Route("/stripe-webhook", stripe_webhook, methods=["POST"]),
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

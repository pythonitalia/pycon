import asyncio
import json
import logging
import subprocess
import sys
from io import StringIO

from mangum import Mangum
from pythonit_toolkit.sentry.sentry import configure_sentry
from pythonit_toolkit.starlette_backend.pastaporto_backend import on_auth_error
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route

from src.api.views import GraphQL
from src.association.auth import RouterAuthBackend
from src.association.settings import DEBUG, ENV, SENTRY_DSN
from src.database.db import database
from src.webhooks.handlers import run_handler
from src.webhooks.views import pretix_webhook, stripe_webhook

if SENTRY_DSN:
    configure_sentry(dsn=str(SENTRY_DSN), env=ENV)

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine.Engine").disabled = True


app = Starlette(
    debug=DEBUG,
    routes=[
        Route("/graphql", GraphQL()),
        Route("/stripe-webhook", stripe_webhook, methods=["POST"]),
        Route("/pretix-webhook", pretix_webhook, methods=["POST"]),
    ],
    middleware=[
        Middleware(
            AuthenticationMiddleware,
            backend=RouterAuthBackend(),
            on_error=on_auth_error,
        ),
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


wrapped_app = SentryAsgiMiddleware(app)


async def event_handler(event):
    try:
        await startup()
        await run_handler("crons", event["name"], json.loads(event["payload"]))
    finally:
        await shutdown()


def handler(event, context):
    if command := event.get("_cli_command"):  # noqa
        native_stdout = sys.stdout
        native_stderr = sys.stderr
        output_buffer = StringIO()

        try:
            sys.stdout = output_buffer
            sys.stderr = output_buffer

            if command.get("action") == "migrate":
                result = subprocess.check_output(
                    "python -m alembic upgrade head",
                    shell=True,
                    stderr=subprocess.STDOUT,
                )
                output_buffer.write(_to_native(result))
        finally:
            sys.stdout = native_stdout
            sys.stderr = native_stderr

        return {"output": output_buffer.getvalue()}

    if received_event := event.get("detail"):
        print("event =>", event)
        asyncio.run(event_handler(received_event))
        return

    asgi_handler = Mangum(wrapped_app)
    response = asgi_handler(event, context)
    return response


def _to_native(x, charset=sys.getdefaultencoding(), errors="strict"):  # noqa
    if x is None or isinstance(x, str):
        return x
    return x.decode(charset, errors)

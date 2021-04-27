import logging
import subprocess
import sys
from io import StringIO

from mangum import Mangum
from pythonit_toolkit.starlette_backend.middleware import pastaporto_auth_middleware
from starlette.applications import Starlette
from starlette.routing import Route

from src.api.views import GraphQL
from src.association.settings import DEBUG, PASTAPORTO_SECRET
from src.database.db import database
from src.webhooks.views import stripe_webhook

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine.Engine").disabled = True


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


def handler(event, context):
    if (command := event.get("_cli_command")) :  # noqa
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

    asgi_handler = Mangum(app)
    response = asgi_handler(event, context)
    return response


def _to_native(x, charset=sys.getdefaultencoding(), errors="strict"):  # noqa
    if x is None or isinstance(x, str):
        return x
    return x.decode(charset, errors)

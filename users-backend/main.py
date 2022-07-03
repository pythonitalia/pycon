import logging
import subprocess
import sys
from io import StringIO

from mangum import Mangum
from pythonit_toolkit.sentry.sentry import configure_sentry
from pythonit_toolkit.starlette_backend.middleware import pastaporto_auth_middleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route

from users.api.views import GraphQL
from users.db import get_engine, get_session
from users.domain.repository import UsersRepository
from users.internal_api.views import GraphQL as InternalGraphQL
from users.settings import DEBUG, ENVIRONMENT, PASTAPORTO_SECRET, SECRET_KEY, SENTRY_DSN
from users.social_auth.views import google_login, google_login_auth

if SENTRY_DSN:
    configure_sentry(dsn=str(SENTRY_DSN), env=ENVIRONMENT)

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine.Engine").disabled = True

routes = [
    Route("/graphql", GraphQL()),
    Route("/internal-api", InternalGraphQL()),
    Route("/login/google", google_login),
    Route("/login/google/auth", google_login_auth, name="auth"),
]

app = Starlette(
    debug=DEBUG,
    routes=routes,
    middleware=[
        Middleware(SessionMiddleware, secret_key=str(SECRET_KEY)),
        pastaporto_auth_middleware(str(PASTAPORTO_SECRET)),
    ],
)


@app.middleware("http")
async def repositories_middleware(request, call_next):
    request.state.users_repository = UsersRepository(request.state.session)
    return await call_next(request)


@app.middleware("http")
async def async_session_middleware(request, call_next):
    async with get_session(request.app.state.engine) as session:
        request.state.session = session
        return await call_next(request)


@app.on_event("startup")
async def startup():
    app.state.engine = get_engine()


@app.on_event("shutdown")
async def shutdown():
    await app.state.engine.dispose()


wrapped_app = SentryAsgiMiddleware(app)


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

    asgi_handler = Mangum(wrapped_app)
    response = asgi_handler(event, context)
    return response


def _to_native(x, charset=sys.getdefaultencoding(), errors="strict"):  # noqa
    if x is None or isinstance(x, str):
        return x
    return x.decode(charset, errors)

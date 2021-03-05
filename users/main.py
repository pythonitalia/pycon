import logging
import subprocess
import sys
from io import StringIO

from mangum import Mangum
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route

from users.admin_api.views import GraphQL as AdminGraphQL
from users.api.views import GraphQL
from users.auth.backend import PastaportoAuthBackend, on_auth_error
from users.db import get_engine, get_session
from users.domain.repository import UsersRepository
from users.internal_api.views import GraphQL as InternalGraphQL
from users.settings import DEBUG, SERVICE_TO_SERVICE_SECRET, SESSION_SECRET_KEY
from users.social_auth.views import google_login, google_login_auth

logging.basicConfig(level=logging.INFO)

routes = [
    Route("/graphql", GraphQL()),
    Route("/admin-api", AdminGraphQL()),
    Route("/login/google", google_login),
    Route("/login/google/auth", google_login_auth, name="auth"),
]

if SERVICE_TO_SERVICE_SECRET:
    # Add internal-api route only if the deployment
    # has the service to service key, this should allow
    # us to deploy this code in two separate lambdas, one for
    # internal api requests and another for other usages
    routes.append(Route("/internal-api", InternalGraphQL()))

app = Starlette(
    debug=DEBUG,
    routes=routes,
    middleware=[
        Middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY),
        Middleware(
            AuthenticationMiddleware,
            backend=PastaportoAuthBackend(),
            on_error=on_auth_error,
        ),
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


def handler(event, context):
    if (command := event.get("_cli_command")) :
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

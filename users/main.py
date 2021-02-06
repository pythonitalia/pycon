import logging

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.routing import Route

from users.api.views import GraphQL
from users.auth.backend import JWTAuthBackend, on_auth_error
from users.db import get_engine, get_session
from users.domain.repository import UsersRepository
from users.settings import DEBUG, SESSION_SECRET_KEY
from users.social_auth.views import google_login, google_login_auth

logging.basicConfig(level=logging.INFO)

app = Starlette(
    debug=DEBUG,
    routes=[
        Route("/graphql", GraphQL()),
        Route("/login/google", google_login),
        Route("/login/google/auth", google_login_auth, name="auth"),
    ],
    middleware=[
        Middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY),
        Middleware(
            AuthenticationMiddleware,
            backend=JWTAuthBackend(UsersRepository()),
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

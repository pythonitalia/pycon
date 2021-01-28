from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route
from users.api.views import GraphQL
from users.auth.backend import JWTAuthBackend
from users.settings import DATABASE_URL, DEBUG

app = Starlette(
    debug=DEBUG,
    routes=[Route("/graphql", GraphQL())],
    middleware=[Middleware(AuthenticationMiddleware, backend=JWTAuthBackend())],
)


@app.middleware("http")
async def async_session_middleware(request, call_next):
    async with AsyncSession(request.app.state.engine) as session:
        request.state.session = session

        try:
            return await call_next(request)
        finally:
            # TODO is needed?
            request.state.session = None


@app.on_event("startup")
async def startup():
    app.state.engine = create_async_engine(DATABASE_URL, echo=True)

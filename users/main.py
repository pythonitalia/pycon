from api.views import GraphQL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from starlette.applications import Starlette
from starlette.config import Config
from starlette.routing import Route

config = Config(".env")
DATABASE_URL = config("DATABASE_URL")

app = Starlette(debug=True, routes=[Route("/graphql", GraphQL())])


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

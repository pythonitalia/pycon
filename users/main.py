import databases
from api.views import GraphQL
from starlette.applications import Starlette
from starlette.config import Config
from starlette.routing import Route

config = Config(".env")
DATABASE_URL = config("DATABASE_URL")

database = databases.Database(DATABASE_URL)

app = Starlette(debug=True, routes=[Route("/graphql", GraphQL())])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

from sqlalchemy.engine import create_engine
from ward import fixture

from association.settings import DATABASE_URL
from database.db import database, metadata

engine = create_engine(DATABASE_URL)

_DB_CONNECTED = False


@fixture
async def db():
    global _DB_CONNECTED

    if not _DB_CONNECTED:
        await database.connect()
        _DB_CONNECTED = True

    metadata.drop_all(engine)
    metadata.create_all(engine)

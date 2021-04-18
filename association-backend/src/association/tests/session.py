from sqlalchemy.engine import create_engine
from ward import fixture

from src.association.settings import DATABASE_URL
from src.database.db import database, metadata

engine = create_engine(DATABASE_URL)


@fixture
async def db():
    if not database.is_connected:
        await database.connect()

    metadata.drop_all(engine)
    metadata.create_all(engine)

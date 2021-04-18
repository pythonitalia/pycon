# isort: off
import asyncio
import os
import sys
from sqlalchemy.engine import create_engine

from sqlalchemy.engine.url import make_url  # noqa

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))  # noqa

from db_utils import create_database, database_exists

from database.db import metadata
from association.settings import DATABASE_URL


async def run():
    db_name = make_url(DATABASE_URL).database
    sync_database_url = DATABASE_URL.replace("asyncpg", "psycopg2").replace("TEST_", "")
    engine = create_engine(sync_database_url)

    if not database_exists(sync_database_url, db_name):
        create_database(sync_database_url, db_name)
        metadata.create_all(engine)
    else:
        metadata.drop_all(engine)
        metadata.create_all(engine)


if __name__ == "__main__":
    asyncio.run(run())
